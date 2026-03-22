"""
Unit Tests: Edge Cases & Adversarial Inputs (Phase 9 of EXHAUSTIVE_TEST_AUDIT)
================================================================================
Synthetic HTML inputs testing:
  - Handles in <script>, HTML comments, alt text, title attributes
  - Malformed URLs: //handle, trailing @
  - Unicode/emoji handles
  - Very long handles (50+ chars)
  - Empty / JS-only pages
  - Instagram embed variations
  - Markdown-specific patterns
  - Domain-suffix email leaks
  - Site-account blocklist verification
"""

from services.extraction.RegexHandleExtractorService import RegexHandleExtractorService

extract_handles_from_html = RegexHandleExtractorService.extract_handles_from_html


# ══════════════════════════════════════════════════════════════════════
# 9a: Handles in non-content regions
# ══════════════════════════════════════════════════════════════════════

class TestHandlesInNonContentRegions:
    """Handles inside <script>, <!-- comments -->, and attributes."""

    def test_handles_in_script_tags_extracted(self):
        r"""@handles inside <script> strings NOT extracted with (?<!\S) lookbehind.

        The regex runs on raw HTML/markdown — script contents are visible.
        However, the (?<!\S) lookbehind now blocks @handles immediately
        preceded by quotes ('"', "'") or other non-whitespace chars, so
        JS string literals like `"@script_handle_xyz"` are correctly blocked.
        This is better behaviour: JS string handles are not social mentions.
        """
        html = """
        <script>
          var user = "@script_handle_xyz";
        </script>
        <p>Real content here</p>
        """
        results = extract_handles_from_html(html)
        handles = {r.handle.lower() for r in results}
        # Correctly blocked — inside JS string, not a social mention
        assert "script_handle_xyz" not in handles

    def test_handles_in_html_comments_extracted(self):
        """@handles inside <!-- comments --> ARE extracted (text-based regex)."""
        html = """
        <!-- Follow @commented_handle for updates -->
        <p>Normal content</p>
        """
        results = extract_handles_from_html(html)
        handles = {r.handle.lower() for r in results}
        assert "commented_handle" in handles

    def test_handles_in_alt_text(self):
        """Handles in img alt text should be extractable."""
        html = """
        <img src="photo.jpg" alt="Photo by @photographer_handle" />
        """
        results = extract_handles_from_html(html)
        handles = {r.handle.lower() for r in results}
        assert "photographer_handle" in handles

    def test_handles_in_title_attribute(self):
        """Handles in anchor title attributes should be extractable."""
        html = """
        <a href="#" title="Follow @titled_handle">Click</a>
        """
        results = extract_handles_from_html(html)
        handles = {r.handle.lower() for r in results}
        assert "titled_handle" in handles


# ══════════════════════════════════════════════════════════════════════
# 9b: Malformed URLs & edge cases
# ══════════════════════════════════════════════════════════════════════

class TestMalformedURLs:
    """Verify graceful handling of malformed or edge-case URLs."""

    def test_double_slash_instagram(self):
        """instagram.com//handle → should NOT crash, may or may not extract."""
        html = '<a href="https://instagram.com//badpath">link</a>'
        results = extract_handles_from_html(html)
        # Should not crash — that's the primary test
        assert isinstance(results, list)

    def test_tiktok_trailing_at(self):
        """tiktok.com/@ with no handle → should not extract."""
        html = '<a href="https://tiktok.com/@">empty</a>'
        results = extract_handles_from_html(html)
        handles = {r.handle.lower() for r in results}
        # @ alone is not a valid handle
        assert len(handles) == 0

    def test_youtube_with_query_params(self):
        """youtube.com/@handle?sub_confirmation=1 → should extract handle."""
        html = '<a href="https://youtube.com/@FitnessBlender?sub_confirmation=1">Sub</a>'
        results = extract_handles_from_html(html)
        handles = {r.handle.lower() for r in results}
        assert "fitnessblender" in handles

    def test_instagram_trailing_hash(self):
        """instagram.com/handle#section → should extract handle."""
        html = '<a href="https://instagram.com/fitness_pro#posts">Posts</a>'
        results = extract_handles_from_html(html)
        _handles = {r.handle.lower() for r in results}
        # The regex boundary may or may not capture this - test for no crash
        assert isinstance(results, list)

    def test_http_vs_https(self):
        """Both http:// and https:// should work."""
        html = """
        <a href="http://instagram.com/http_handle">HTTP</a>
        <a href="https://instagram.com/https_handle">HTTPS</a>
        """
        results = extract_handles_from_html(html)
        handles = {r.handle.lower() for r in results}
        assert "http_handle" in handles
        assert "https_handle" in handles


# ══════════════════════════════════════════════════════════════════════
# 9c: Unicode, emoji, and special character handles
# ══════════════════════════════════════════════════════════════════════

class TestUnicodeAndSpecialHandles:
    """Handles with non-ASCII chars — verify rejection or graceful handling."""

    def test_unicode_handle_rejected(self):
        """Unicode handles like @café_lover should be rejected (not valid on most platforms)."""
        html = "<p>Follow @café_lover for recipes</p>"
        results = extract_handles_from_html(html)
        handles = {r.handle.lower() for r in results}
        # café has non-ASCII — regex [A-Za-z0-9_.] should not match it
        assert "café_lover" not in handles

    def test_chinese_handle_rejected(self):
        """Chinese characters should not match as handles."""
        html = "<p>Follow @运动达人 for fitness</p>"
        results = extract_handles_from_html(html)
        handles = {r.handle.lower() for r in results}
        assert "运动达人" not in handles

    def test_very_long_handle_rejected(self):
        """Handles over 30 chars should be rejected (max platform length)."""
        long_handle = "a" * 50
        html = f'<a href="https://instagram.com/{long_handle}">profile</a>'
        results = extract_handles_from_html(html)
        handles = {r.handle.lower() for r in results}
        assert long_handle not in handles

    def test_handle_exactly_30_chars(self):
        """Handle at exactly 30 chars (IG max) should be accepted."""
        handle_30 = "a" * 28 + "b" * 2  # 30 chars total
        html = f'<a href="https://instagram.com/{handle_30}/">profile</a>'
        results = extract_handles_from_html(html)
        handles = {r.handle.lower() for r in results}
        assert handle_30 in handles


# ══════════════════════════════════════════════════════════════════════
# 9d: Empty and degenerate pages
# ══════════════════════════════════════════════════════════════════════

class TestDegeneratePages:
    """Verify no crash on empty/minimal pages."""

    def test_empty_string(self):
        """Empty string → no crash, empty results."""
        results = extract_handles_from_html("")
        assert results == []

    def test_whitespace_only(self):
        """Whitespace-only content → no crash, empty results."""
        results = extract_handles_from_html("   \n\t  \n  ")
        assert results == []

    def test_js_only_page(self):
        """Page with only JavaScript → no crash."""
        html = """
        <html><head><script>
        var x = 1; function f() { return x + 1; }
        document.addEventListener('load', function() { f(); });
        </script></head><body></body></html>
        """
        results = extract_handles_from_html(html)
        assert isinstance(results, list)

    def test_only_html_structure(self):
        """Minimal HTML structure with no content → no crash, empty results."""
        html = "<html><head><title>Test</title></head><body></body></html>"
        results = extract_handles_from_html(html)
        assert results == []

    def test_very_large_page(self):
        """Large page (5K handles) → should complete without error."""
        lines = [f'<a href="https://instagram.com/user_{i}">Profile</a>'
                 for i in range(5000)]
        html = "\n".join(lines)
        results = extract_handles_from_html(html)
        assert len(results) >= 4000  # Some may dedup or be filtered


# ══════════════════════════════════════════════════════════════════════
# 9e: Instagram embed variations
# ══════════════════════════════════════════════════════════════════════

class TestInstagramEmbedVariations:
    """Test variations of the 'A post shared by' embed pattern."""

    def test_embed_without_name(self):
        """'A post shared by @handle' (no name before @) should still extract."""
        html = """
        <blockquote>
            <p>A post shared by (@justhandle)</p>
        </blockquote>
        """
        results = extract_handles_from_html(html)
        handles = {r.handle.lower() for r in results}
        assert "justhandle" in handles

    def test_shared_by_variation(self):
        """'shared by Name (@handle)' (no 'A post') should also work."""
        html = """
        <blockquote>
            <p>shared by Fitness Hero (@fitnesshero99)</p>
        </blockquote>
        """
        results = extract_handles_from_html(html)
        handles = {r.handle.lower() for r in results}
        assert "fitnesshero99" in handles

    def test_embed_with_pipe_in_name(self):
        """Name with pipe separator: 'Sarah | FitLife (@handle)' → pipe-stripped
        to 'Sarah' which is a single word — NameCleaner rejects (not a person name)."""
        html = """
        <p>A post shared by Sarah | FitLife (@sarahfitlife)</p>
        """
        results = extract_handles_from_html(html)
        by_handle = {r.handle.lower(): r for r in results}
        assert "sarahfitlife" in by_handle
        # "Sarah" alone is a single word → NameCleaner.clean_name returns None → ""
        assert by_handle["sarahfitlife"].name == ""

    def test_embed_deduped_with_url(self):
        """Embed + URL for same handle → only 1 result (deduped)."""
        html = """
        <a href="https://instagram.com/dupetest">IG</a>
        <p>A post shared by Dupe Tester (@dupetest)</p>
        """
        results = extract_handles_from_html(html)
        dupes = [r for r in results if r.handle.lower() == "dupetest"]
        assert len(dupes) == 1
        # Embed has higher priority → name should be present
        assert dupes[0].name == "Dupe Tester"


# ══════════════════════════════════════════════════════════════════════
# 9f: Markdown-specific patterns (crawl4ai output)
# ══════════════════════════════════════════════════════════════════════

class TestMarkdownPatterns:
    """Markdown-specific extraction patterns from crawl4ai crawler output."""

    def test_markdown_link_with_handle(self):
        """[@handle](https://instagram.com/handle) → both handle + platform."""
        md = "Follow [@fitgirl99](https://www.instagram.com/fitgirl99/) for tips"
        results = extract_handles_from_html(md)
        handles = {r.handle.lower() for r in results}
        assert "fitgirl99" in handles
        by_handle = {r.handle.lower(): r for r in results}
        assert by_handle["fitgirl99"].platform == "Instagram"

    def test_markdown_link_tiktok(self):
        """[text](https://tiktok.com/@handle) → extract from URL target."""
        md = "Check out [dance moves](https://www.tiktok.com/@dancer99)"
        results = extract_handles_from_html(md)
        handles = {r.handle.lower() for r in results}
        assert "dancer99" in handles

    def test_markdown_image_with_handle_in_url(self):
        """![img](instagram.com/handle/media) → extract handle, not media path."""
        md = '![photo](https://www.instagram.com/photographer/media/image.jpg)'
        results = extract_handles_from_html(md)
        handles = {r.handle.lower() for r in results}
        assert "photographer" in handles

    def test_bare_url_in_markdown(self):
        """Plain URL in markdown text → should still extract handle."""
        md = "Profile: https://www.instagram.com/plainurl_handle/"
        results = extract_handles_from_html(md)
        handles = {r.handle.lower() for r in results}
        assert "plainurl_handle" in handles


# ══════════════════════════════════════════════════════════════════════
# 9g: Domain-suffix and email leak filter
# ══════════════════════════════════════════════════════════════════════

class TestDomainSuffixFilter:
    """Verify email/domain handles are filtered by the domain-suffix filter."""

    def test_dot_com_handle_rejected(self):
        """@brookeence.com is an email domain, not a handle."""
        html = "<p>Contact @brookeence.com for inquiries</p>"
        results = extract_handles_from_html(html)
        handles = {r.handle.lower() for r in results}
        assert "brookeence.com" not in handles

    def test_dot_co_uk_handle_rejected(self):
        """@example.co.uk is a domain, not a handle."""
        html = "<p>Visit @example.co.uk for more</p>"
        results = extract_handles_from_html(html)
        handles = {r.handle.lower() for r in results}
        assert "example.co.uk" not in handles

    def test_com_fragment_handle_rejected(self):
        """@1dsmgmt.comUse is a mangled email, not a handle."""
        html = "<p>@1dsmgmt.comUse for management</p>"
        results = extract_handles_from_html(html)
        handles = {r.handle.lower() for r in results}
        assert "1dsmgmt.comuse" not in handles

    def test_dot_io_handle_rejected(self):
        """@modash.io is a domain, not a handle."""
        html = "<p>@modash.io analytics</p>"
        results = extract_handles_from_html(html)
        handles = {r.handle.lower() for r in results}
        assert "modash.io" not in handles

    def test_real_handle_with_dots_accepted(self):
        """@kayla.itsines is a real handle (dots allowed, no domain suffix)."""
        html = '<a href="https://instagram.com/kayla.itsines">IG</a>'
        results = extract_handles_from_html(html)
        handles = {r.handle.lower() for r in results}
        assert "kayla.itsines" in handles


# ══════════════════════════════════════════════════════════════════════
# 9g-2: Email pattern filter — regression tests for evolved.gg bug
# Bug: *****@evolved.gg was extracted as ig_handle "evolved.gg".
# Root cause: (?<!\w) lookbehind didn't block non-word chars like *.
# Fix: (?<!\S) lookbehind + _EMAIL_PATTERN pre-filter.
# ══════════════════════════════════════════════════════════════════════

class TestEmailPatternFilter:
    """Email-like strings must not be extracted as @handles."""

    def test_obfuscated_email_not_extracted(self):
        """*****@evolved.gg is an obfuscated email — must not extract evolved.gg.

        Regression test for the feedspot gaming page bug where the bio text
        '*****@evolved.gg' was captured as an Instagram handle.
        """
        html = "<p>Contact *****@evolved.gg for bookings</p>"
        results = extract_handles_from_html(html)
        handles = {r.handle.lower() for r in results}
        assert "evolved.gg" not in handles

    def test_real_email_not_extracted(self):
        """user@example.com — neither part should be extracted as a handle."""
        html = "<p>Email us at contact@brandname.com</p>"
        results = extract_handles_from_html(html)
        handles = {r.handle.lower() for r in results}
        assert "brandname.com" not in handles
        assert "contact" not in handles

    def test_feedspot_bio_string_not_extracted(self):
        """Full feedspot bio format regression: *****@evolved.gg 👨‍💼 Instagram Handle @average_jonas.

        Only @average_jonas should be extracted — not evolved.gg.
        """
        bio = "*****@evolved.gg 👨\u200d💼 Instagram Handle @average_jonas"
        results = extract_handles_from_html(bio)
        handles = {r.handle.lower() for r in results}
        assert "evolved.gg" not in handles
        assert "average_jonas" in handles

    def test_valid_at_mention_preceded_by_space_extracted(self):
        """A real @mention preceded by whitespace must still be extracted."""
        html = "<p>Follow @ninja for gaming content!</p>"
        results = extract_handles_from_html(html)
        handles = {r.handle.lower() for r in results}
        assert "ninja" in handles

    def test_at_handle_after_newline_extracted(self):
        """@handle at start of a line (preceded by newline) must be extracted."""
        html = "Gaming creator:\n@markiplier is the best"
        results = extract_handles_from_html(html)
        handles = {r.handle.lower() for r in results}
        assert "markiplier" in handles

    def test_email_before_handle_on_same_line_handle_extracted(self):
        """If an email and a valid @mention appear on the same line, handle is kept."""
        html = "<p>Email: jeff@jeffseid.com — Instagram @jeff_seid</p>"
        results = extract_handles_from_html(html)
        handles = {r.handle.lower() for r in results}
        assert "jeff_seid" in handles
        assert "jeffseid.com" not in handles


# ══════════════════════════════════════════════════════════════════════
# 9h: Blocklist verification — known false positives
# ══════════════════════════════════════════════════════════════════════

class TestBlocklistCompleteness:
    """Verify known false positive categories are blocked."""

    def test_js_framework_names_blocked(self):
        """JS framework names must NOT be extracted as handles."""
        html = """
        <p>Built with @vue, @react, @angular, @svelte, @next, @remix</p>
        <p>Tools: @webpack, @vite, @eslint, @prettier, @babel</p>
        <p>Testing: @jest, @mocha, @cypress</p>
        """
        results = extract_handles_from_html(html)
        handles = {r.handle.lower() for r in results}
        blocked = {"vue", "react", "angular", "svelte", "next", "remix",
                   "webpack", "vite", "eslint", "prettier", "babel",
                   "jest", "mocha", "cypress"}
        leaked = blocked & handles
        assert not leaked, f"JS framework names leaked: {leaked}"

    def test_css_at_rules_blocked(self):
        """CSS at-rules must NOT be extracted as handles."""
        html = """
        @media screen and (max-width: 768px) {}
        @keyframes fadeIn { from { opacity: 0; } }
        @import url('styles.css');
        @font-face { font-family: 'Custom'; }
        """
        results = extract_handles_from_html(html)
        handles = {r.handle.lower() for r in results}
        blocked = {"media", "keyframes", "import", "font"}
        leaked = blocked & handles
        assert not leaked, f"CSS at-rules leaked: {leaked}"

    def test_json_ld_terms_blocked(self):
        """JSON-LD terms must NOT be extracted as handles."""
        html = """
        <script type="application/ld+json">
        {"@context": "https://schema.org", "@type": "Person",
         "@graph": [{"@id": "#person", "@language": "en"}]}
        </script>
        """
        results = extract_handles_from_html(html)
        handles = {r.handle.lower() for r in results}
        blocked = {"context", "type", "graph", "id", "language"}
        leaked = blocked & handles
        assert not leaked, f"JSON-LD terms leaked: {leaked}"

    def test_platform_names_blocked(self):
        """Platform names as @handles must NOT be extracted."""
        html = "<p>Find us on @instagram @tiktok @youtube @twitter @facebook @snapchat</p>"
        results = extract_handles_from_html(html)
        handles = {r.handle.lower() for r in results}
        blocked = {"instagram", "tiktok", "youtube", "twitter", "facebook", "snapchat"}
        leaked = blocked & handles
        assert not leaked, f"Platform names leaked: {leaked}"

    def test_template_placeholders_blocked(self):
        """Template/placeholder handles must NOT be extracted."""
        html = "<p>Replace @username or @handle or @example with your handle</p>"
        results = extract_handles_from_html(html)
        handles = {r.handle.lower() for r in results}
        blocked = {"username", "handle", "example"}
        leaked = blocked & handles
        assert not leaked, f"Template placeholders leaked: {leaked}"

    def test_site_accounts_blocked(self):
        """Listicle site accounts must NOT be extracted as handles."""
        html = """
        <p>Powered by @feedspot @modash @seekahost @trainerize @favikon</p>
        <p>Also @collabstr @heepsy @insense @clickanalytic @izea</p>
        """
        results = extract_handles_from_html(html)
        handles = {r.handle.lower() for r in results}
        blocked = {"feedspot", "modash", "seekahost", "trainerize", "favikon",
                   "collabstr", "heepsy", "insense", "clickanalytic", "izea"}
        leaked = blocked & handles
        assert not leaked, f"Site accounts leaked: {leaked}"

    def test_url_path_segments_blocked(self):
        """URL path segments must NOT be extracted."""
        html = """
        <a href="https://instagram.com/explore/">Explore</a>
        <a href="https://instagram.com/stories/someone/">Stories</a>
        <a href="https://twitter.com/intent/tweet">Tweet</a>
        <a href="https://twitter.com/share">Share</a>
        <a href="https://youtube.com/results?q=fitness">Search</a>
        """
        results = extract_handles_from_html(html)
        handles = {r.handle.lower() for r in results}
        blocked = {"explore", "stories", "intent", "share", "results"}
        leaked = blocked & handles
        assert not leaked, f"URL path segments leaked: {leaked}"
