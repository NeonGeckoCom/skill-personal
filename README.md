# <img src='https://0000.us/klatchat/app/files/neon_images/icons/neon_skill.png' card_color="#FF8600" width="50" style="vertical-align:bottom">Personal

## Summary

Skill used for introduction between the user and Neon.

## Requirements

No special required packages for this skill.

## Description

Personal skill is responsible for introductions and information-acquiring communications between Neon and the user. Neon will use it to introduce himself, explain what and who he is, where he was born, and when it happened. In addition, it will obtain the user’s full, partial, or just a first name, along with the email address, in order to use it for coupons and transcriptions.

## Examples

Ask Neon any question you would like to learn the answer to, such as `where were you born`, `who are you`, `when were you born`. Neon will prompt you to learn more information about you in return, so he can address you by your first name later down the road. Alternatively, you can introduce yourself by saying `Neon my name is` and waiting for a reply.
- who are you
- who made you
- my name is...
- my email address is...
- my klat username is...
- my password is...

## Location

    ${skills}/personal.neon

## Files

    ${skills}/personal.neon/__init__.py  
    ${skills}/personal.neon/test  
    ${skills}/personal.neon/test/intent  
    ${skills}/personal.neon/test/intent/name_profile.intent.json  
    ${skills}/personal.neon/test/intent/who.are.you.intent.json  
    ${skills}/personal.neon/test/intent/who.made.you.intent.json  
    ${skills}/personal.neon/test/intent/emailaddr.intent.json  
    ${skills}/personal.neon/test/intent/when.were.you.born.intent.json  
    ${skills}/personal.neon/test/intent/what.are.you.intent.json  
    ${skills}/personal.neon/test/intent/where.were.you.born.intent.json  
    ${skills}/personal.neon/settings.json  
    ${skills}/personal.neon/dialog  
    ${skills}/personal.neon/dialog/en-us  
    ${skills}/personal.neon/dialog/en-us/who.made.me.dialog  
    ${skills}/personal.neon/dialog/en-us/when.was.i.born.dialog  
    ${skills}/personal.neon/dialog/en-us/where.was.i.born.dialog  
    ${skills}/personal.neon/dialog/en-us/who.am.i.dialog  
    ${skills}/personal.neon/dialog/en-us/what.am.i.dialog  
    ${skills}/personal.neon/regex  
    ${skills}/personal.neon/regex/en-us  
    ${skills}/personal.neon/regex/en-us/profile.rx  
    ${skills}/personal.neon/regex/en-us/emailaddr.rx  
    ${skills}/personal.neon/vocab  
    ${skills}/personal.neon/vocab/en-us  
    ${skills}/personal.neon/vocab/en-us/WhenWereYouBornKeyword.voc  
    ${skills}/personal.neon/vocab/en-us/WhatAreYouKeyword.voc  
    ${skills}/personal.neon/vocab/en-us/What.voc  
    ${skills}/personal.neon/vocab/en-us/no.voc  
    ${skills}/personal.neon/vocab/en-us/AgreementKeyword.voc  
    ${skills}/personal.neon/vocab/en-us/WhereWereYouBornKeyword.voc  
    ${skills}/personal.neon/vocab/en-us/email.voc  
    ${skills}/personal.neon/vocab/en-us/WhoAreYouKeyword.voc  
    ${skills}/personal.neon/vocab/en-us/Neon.voc  
    ${skills}/personal.neon/vocab/en-us/name.voc  
    ${skills}/personal.neon/vocab/en-us/Name.voc  
    ${skills}/personal.neon/vocab/en-us/WhoMadeYouKeyword.voc  
    ${skills}/personal.neon/vocab/en-us/First.voc  
    ${skills}/personal.neon/README.md

  

## Class Diagram

[Click here](https://0000.us/klatchat/app/files/neon_images/class_diagrams/personal.png)

## Available Intents
<details>
<summary>Click to expand.</summary>
<br>

### WhenWereYouBornKeyword.voc  

    when were you born  
    when were you created
      
### WhatAreYouKeyword.voc 
 
    what are you  
    what is neon  
      
### What.voc  
    what is my  
    tell me my 
     
### no.voc  
    no it is  not  
    no  
    incorrect  
    try again  
    
### AgreementKeyword.voc  
    yes  
    sure  
    proceed  
    continue  
    begin  
    start  
    go ahead  
    go  
    lets do it  
    do it  
    of course  
    actually do  
    do  
    i did  
    changed  
    changed my mind  
      
### WhereWereYouBornKeyword.voc  
    where were you born  
    where were you created  
      
### email.voc  
    email address  
    
### WhoAreYouKeyword.voc  
    who are you  
    what is your name  
      
### Neon.voc  
    neon  
    leon  
    nyan  
    
### name.voc  
    My name is  
    
### Name.voc  
    name  
    
### WhoMadeYouKeyword.voc  
    who made you  
    who were you made by  
    who created you  
    who built you  
      
### First.voc  
    first  
    second  
    last  
    middle  
    full

</details>

## Details

### Text

        who are you
        >> My name is Neon. I am an artificial intelligence personal assistant augmented with Neon Gecko dot com Inc copyrighted code and CPI Corp patented technology.

### Picture

### Video

  

## Contact Support

Use the [link](https://neongecko.com/ContactUs) or [submit an issue on GitHub](https://help.github.com/en/articles/creating-an-issue)

## Credits
[Mycroft AI](https://github.com/MycroftAI)
[NeonDaniel](https://github.com/NeonDaniel)
[reginaneon](https://github.com/reginaneon)
