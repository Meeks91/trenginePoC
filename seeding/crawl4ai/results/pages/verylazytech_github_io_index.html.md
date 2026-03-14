# Google Dorks for Bug Bounty - By VeryLazyTech
Enter a domain:
  * Join Slack Channels
[ext:pdf "invite" "join.slack" site:"example.com"](https://www.google.com/search?q=ext%3Apdf%20%22invite%22%20%22join.slack%22%20site%3A%22example.com%22)
  * Broad domain search w/ negative search
[site:"example.com" -www -shop -share -ir -mfa](https://www.google.com/search?q=site%3A%22example.com%22%20-www%20-shop%20-share%20-ir%20-mfa)
  * PHP extension w/ parameters
[site:"example.com" ext:php inurl:?](https://www.google.com/search?q=site%3A%22example.com%22%20ext%3Aphp%20inurl%3A%3F)
  * API Endpoints
[site:"example[.]com" inurl:api | site:*/rest | site:*/v1 | site:*/v2 | site:*/v3](https://www.google.com/search?q=site%3A%22example%5B.%5Dcom%22%20inurl%3Aapi%20%7C%20site%3A*%2Frest%20%7C%20site%3A*%2Fv1%20%7C%20site%3A*%2Fv2%20%7C%20site%3A*%2Fv3)
  * Juicy Extensions
[site:"example[.]com" ext:log | ext:txt | ext:conf | ext:cnf | ext:ini | ext:env | ext:sh | ext:bak | ext:backup | ext:swp | ext:old | ext:~ | ext:git | ext:svn | ext:htpasswd | ext:htaccess | ext:json](https://www.google.com/search?q=site%3A%22example%5B.%5Dcom%22%20ext%3Alog%20%7C%20ext%3Atxt%20%7C%20ext%3Aconf%20%7C%20ext%3Acnf%20%7C%20ext%3Aini%20%7C%20ext%3Aenv%20%7C%20ext%3Ash%20%7C%20ext%3Abak%20%7C%20ext%3Abackup%20%7C%20ext%3Aswp%20%7C%20ext%3Aold%20%7C%20ext%3A~%20%7C%20ext%3Agit%20%7C%20ext%3Asvn%20%7C%20ext%3Ahtpasswd%20%7C%20ext%3Ahtaccess%20%7C%20ext%3Ajson)
  * High % inurl keywords
[inurl:conf | inurl:env | inurl:cgi | inurl:bin | inurl:etc | inurl:root | inurl:sql | inurl:backup | inurl:admin | inurl:php site:"example[.]com"](https://www.google.com/search?q=inurl%3Aconf%20%7C%20inurl%3Aenv%20%7C%20inurl%3Acgi%20%7C%20inurl%3Abin%20%7C%20inurl%3Aetc%20%7C%20inurl%3Aroot%20%7C%20inurl%3Asql%20%7C%20inurl%3Abackup%20%7C%20inurl%3Aadmin%20%7C%20inurl%3Aphp%20site%3A%22example%5B.%5Dcom%22)
  * Server Errors
[inurl:"error" | intitle:"exception" | intitle:"failure" | intitle:"server at" | inurl:exception | "database error" | "SQL syntax" | "undefined index" | "unhandled exception" | "stack trace" site:"example[.]com"](https://www.google.com/search?q=inurl%3A%22error%22%20%7C%20intitle%3A%22exception%22%20%7C%20intitle%3A%22failure%22%20%7C%20intitle%3A%22server%20at%22%20%7C%20inurl%3Aexception%20%7C%20%22database%20error%22%20%7C%20%22SQL%20syntax%22%20%7C%20%22undefined%20index%22%20%7C%20%22unhandled%20exception%22%20%7C%20%22stack%20trace%22%20site%3A%22example%5B.%5Dcom%22)
  * XSS prone parameters
[inurl:q= | inurl:s= | inurl:search= | inurl:query= | inurl:keyword= | inurl:lang= inurl:& site:"example.com"](https://www.google.com/search?q=inurl%3Aq%3D%20%7C%20inurl%3As%3D%20%7C%20inurl%3Asearch%3D%20%7C%20inurl%3Aquery%3D%20%7C%20inurl%3Akeyword%3D%20%7C%20inurl%3Alang%3D%20inurl%3A%26%20site%3A%22example.com%22)
  * Open Redirect prone parameters
[inurl:url= | inurl:return= | inurl:next= | inurl:redirect= | inurl:redir= | inurl:ret= | inurl:r2= | inurl:page= inurl:& inurl:http site:"example.com"](https://www.google.com/search?q=inurl%3Aurl%3D%20%7C%20inurl%3Areturn%3D%20%7C%20inurl%3Anext%3D%20%7C%20inurl%3Aredirect%3D%20%7C%20inurl%3Aredir%3D%20%7C%20inurl%3Aret%3D%20%7C%20inurl%3Ar2%3D%20%7C%20inurl%3Apage%3D%20inurl%3A%26%20inurl%3Ahttp%20site%3A%22example.com%22)
  * SQLi Prone Parameters
[inurl:id= | inurl:pid= | inurl:category= | inurl:cat= | inurl:action= | inurl:sid= | inurl:dir= inurl:& site:"example.com"](https://www.google.com/search?q=inurl%3Aid%3D%20%7C%20inurl%3Apid%3D%20%7C%20inurl%3Acategory%3D%20%7C%20inurl%3Acat%3D%20%7C%20inurl%3Aaction%3D%20%7C%20inurl%3Asid%3D%20%7C%20inurl%3Adir%3D%20inurl%3A%26%20site%3A%22example.com%22)
  * SSRF Prone Parameters
[inurl:http | inurl:url= | inurl:path= | inurl:dest= | inurl:html= | inurl:data= | inurl:domain= | inurl:page= inurl:& site:"example.com"](https://www.google.com/search?q=inurl%3Ahttp%20%7C%20inurl%3Aurl%3D%20%7C%20inurl%3Apath%3D%20%7C%20inurl%3Adest%3D%20%7C%20inurl%3Ahtml%3D%20%7C%20inurl%3Adata%3D%20%7C%20inurl%3Adomain%3D%20%20%7C%20inurl%3Apage%3D%20inurl%3A%26%20site%3A%22example.com%22)
  * LFI Prone Parameters
[inurl:include | inurl:dir | inurl:detail= | inurl:file= | inurl:folder= | inurl:inc= | inurl:locate= | inurl:doc= | inurl:conf= inurl:& site:"example.com"](https://www.google.com/search?q=inurl%3Ainclude%20%7C%20inurl%3Adir%20%7C%20inurl%3Adetail%3D%20%7C%20inurl%3Afile%3D%20%7C%20inurl%3Afolder%3D%20%7C%20inurl%3Ainc%3D%20%7C%20inurl%3Alocate%3D%20%7C%20inurl%3Adoc%3D%20%7C%20inurl%3Aconf%3D%20inurl%3A%26%20site%3A%22example.com%22)
  * RCE Prone Parameters
[inurl:cmd | inurl:exec= | inurl:query= | inurl:code= | inurl:do= | inurl:run= | inurl:read= | inurl:ping= inurl:& site:"example.com"](https://www.google.com/search?q=inurl%3Acmd%20%7C%20inurl%3Aexec%3D%20%7C%20inurl%3Aquery%3D%20%7C%20inurl%3Acode%3D%20%7C%20inurl%3Ado%3D%20%7C%20inurl%3Arun%3D%20%7C%20inurl%3Aread%3D%20%20%7C%20inurl%3Aping%3D%20inurl%3A%26%20site%3A%22example.com%22)
  * File upload endpoints
[site:"example.com" ”choose file”](https://www.google.com/search?q=site%3A%22example.com%22%20%E2%80%9Dchoose%20file%E2%80%9D)
  * API Docs
[inurl:apidocs | inurl:api-docs | inurl:swagger | inurl:api-explorer site:"example[.]com"](https://www.google.com/search?q=inurl%3Aapidocs%20%7C%20inurl%3Aapi-docs%20%7C%20inurl%3Aswagger%20%7C%20inurl%3Aapi-explorer%20site%3A%22example%5B.%5Dcom%22)
  * Login Pages
[inurl:login | inurl:signin | intitle:login | intitle:signin | inurl:secure site:"example[.]com"](https://www.google.com/search?q=inurl%3Alogin%20%7C%20inurl%3Asignin%20%7C%20intitle%3Alogin%20%7C%20intitle%3Asignin%20%7C%20inurl%3Asecure%20site%3A%22example%5B.%5Dcom%22)
  * Test Environments
[inurl:test | inurl:env | inurl:dev | inurl:staging | inurl:sandbox | inurl:debug | inurl:temp | inurl:internal | inurl:demo site:"example.com"](https://www.google.com/search?q=inurl%3Atest%20%7C%20inurl%3Aenv%20%7C%20inurl%3Adev%20%7C%20inurl%3Astaging%20%7C%20inurl%3Asandbox%20%7C%20inurl%3Adebug%20%7C%20inurl%3Atemp%20%7C%20inurl%3Ainternal%20%7C%20inurl%3Ademo%20site%3A%22example.com%22)
  * Sensitive Documents
[site:"example.com" ext:txt | ext:pdf | ext:xml | ext:xls | ext:xlsx | ext:ppt | ext:pptx | ext:doc | ext:docx intext:“confidential” | intext:“Not for Public Release” | intext:”internal use only” | intext:“do not distribute”](https://www.google.com/search?q=site%3A%22example.com%22%20ext%3Atxt%20%7C%20ext%3Apdf%20%7C%20ext%3Axml%20%7C%20ext%3Axls%20%7C%20ext%3Axlsx%20%7C%20ext%3Appt%20%7C%20ext%3Apptx%20%7C%20ext%3Adoc%20%7C%20ext%3Adocx%0Aintext%3A%E2%80%9Cconfidential%E2%80%9D%20%7C%20intext%3A%E2%80%9CNot%20for%20Public%20Release%E2%80%9D%20%7C%20intext%3A%E2%80%9Dinternal%20use%20only%E2%80%9D%20%7C%20intext%3A%E2%80%9Cdo%20not%20distribute%E2%80%9D)
  * Sensitive Parameters
[inurl:email= | inurl:phone= | inurl:password= | inurl:secret= inurl:& site:"example[.]com"](https://www.google.com/search?q=inurl%3Aemail%3D%20%7C%20inurl%3Aphone%3D%20%7C%20inurl%3Apassword%3D%20%7C%20inurl%3Asecret%3D%20inurl%3A%26%20site%3A%22example%5B.%5Dcom%22)
  * Adobe Experience Manager (AEM)
[inurl:/content/usergenerated | inurl:/content/dam | inurl:/jcr:content | inurl:/libs/granite | inurl:/etc/clientlibs | inurl:/content/geometrixx | inurl:/bin/wcm | inurl:/crx/de site:"example[.]com"](https://www.google.com/search?q=inurl%3A%2Fcontent%2Fusergenerated%20%7C%20inurl%3A%2Fcontent%2Fdam%20%7C%20inurl%3A%2Fjcr%3Acontent%20%7C%20inurl%3A%2Flibs%2Fgranite%20%7C%20inurl%3A%2Fetc%2Fclientlibs%20%7C%20inurl%3A%2Fcontent%2Fgeometrixx%20%7C%20inurl%3A%2Fbin%2Fwcm%20%7C%20inurl%3A%2Fcrx%2Fde%20site%3A%22example%5B.%5Dcom%22)
  * Disclosed XSS and Open Redirects
[site:openbugbounty.org inurl:reports intext:"example.com"](https://www.google.com/search?q=site%3Aopenbugbounty.org%20inurl%3Areports%20intext%3A%22example.com%22)
  * Google Groups
[site:groups.google.com "example.com"](https://www.google.com/search?q=site%3Agroups.google.com%20%22example.com%22)
  * Code Leaks
[site:pastebin.com "example.com"](https://www.google.com/search?q=site%3Apastebin.com%20%22example.com%22)
  * [site:jsfiddle.net "example.com"](https://www.google.com/search?q=site%3Ajsfiddle.net%20%22example.com%22)
  * [site:codebeautify.org "example.com"](https://www.google.com/search?q=site%3Acodebeautify.org%20%22example.com%22)
  * [site:codepen.io "example.com"](https://www.google.com/search?q=site%3Acodepen.io%20%22example.com%22)
  * Cloud Storage
[site:s3.amazonaws.com "example.com"](https://www.google.com/search?q=site%3As3.amazonaws.com%20%22example.com%22)
  * [site:blob.core.windows.net "example.com"](https://www.google.com/search?q=site%3Ablob.core.windows.net%20%22example.com%22)
  * [site:googleapis.com "example.com"](https://www.google.com/search?q=site%3Agoogleapis.com%20%22example.com%22)
  * [site:drive.google.com "example.com"](https://www.google.com/search?q=site%3Adrive.google.com%20%22example.com%22)
  * [site:dev.azure.com "example[.]com"](https://www.google.com/search?q=site%3Adev.azure.com%20%22example%5B.%5Dcom%22)
  * [site:onedrive.live.com "example[.]com"](https://www.google.com/search?q=site%3Aonedrive.live.com%20%22example%5B.%5Dcom%22)
  * [site:digitaloceanspaces.com "example[.]com"](https://www.google.com/search?q=site%3Adigitaloceanspaces.com%20%22example%5B.%5Dcom%22)
  * [site:sharepoint.com "example[.]com"](https://www.google.com/search?q=site%3Asharepoint.com%20%22example%5B.%5Dcom%22)
  * [site:s3-external-1.amazonaws.com "example[.]com"](https://www.google.com/search?q=site%3As3-external-1.amazonaws.com%20%22example%5B.%5Dcom%22)
  * [site:s3.dualstack.us-east-1.amazonaws.com "example[.]com"](https://www.google.com/search?q=site%3As3.dualstack.us-east-1.amazonaws.com%20%22example%5B.%5Dcom%22)
  * [site:dropbox.com/s "example[.]com"](https://www.google.com/search?q=site%3Adropbox.com%2Fs%20%22example%5B.%5Dcom%22)
  * [site:box.com/s "example[.]com"](https://www.google.com/search?q=site%3Abox.com%2Fs%20%22example%5B.%5Dcom%22)
  * [site:docs.google.com inurl:"/d/" "example[.]com"](https://www.google.com/search?q=site%3Adocs.google.com%20inurl%3A%22%2Fd%2F%22%20%22example%5B.%5Dcom%22)
  * JFrog Artifactory
[site:jfrog.io "example[.]com"](https://www.google.com/search?q=site%3Ajfrog.io%20%22example%5B.%5Dcom%22)
  * Firebase
[site:firebaseio.com "example[.]com"](https://www.google.com/search?q=site%3Afirebaseio.com%20%22example%5B.%5Dcom%22)


