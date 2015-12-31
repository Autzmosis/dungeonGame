##Yet to be named dungeon game
###**By Autzmosis**
####**Coded by タダノデーモン (tadanodaemon)**

####GUI has been updated to kivy, if you would like to test it out you must do the below things:
* Download repository
* Install python2 https://www.python.org/downloads/
* Install kivy http://kivy.org/docs/installation/installation.html
* Run main.py from terminal or command prompt

#####Visit the dropbox folder, for videos the current GUI: https://www.dropbox.com/sh/px7he1pssd3fv48/AAABccXOwlWEoe4dJcRMsF93a?dl=0

The purpose of this project is simply to make an expandable dungeon game using python. It will be
made into an app later. For the basic story line, there will be about ten different dungeons. 

Since this is a text adventure we will need to make methods that recognize typed words, like
'look' or 'walk'. _unique_ and basic features are listed below:

######_Unique_
* _Player starts in a dream that contains the tutorial_
* _Temporary companions_
* _Upgrade Points as stats currency_

######Basic
* Text recognition
* Player learns about their world as they progress (Dark Souls like storytelling)
* 3 Character classes (Rogue, Warrior, Mage)
* 3 Different enemies per dungeon
* Multipule Bosses
* 10 Dungeons
* Storyline
* Sprites and backgrounds

####Special Abilities for the character classes are as follows:
* Rogue - Dual Blitz: Hits target twice with regular attack.
* Warrior - Beserk: Increased damage and lower defense at a low health.
* Mage - Drain: Siphon SP on physical attack. (Scales with atk stat?)
* All special abilities will be randomly used (the player will not choose when to use this, this will be decided by Luck)

###Proposed starter attacks for each character class:
<table border=3px>
<tr>
<td> <b>Rogue</b>  </td><td> <b>Warrior</b>  </td><td> <b>Mage</b>  </td>
</tr>
<tr>
<td> Shank </td><td> Slash </td><td> Knock </td>
</tr>
<tr>
<td> Smokescreen </td><td> Sheild Bash </td><td> Magic Blast </td>
</tr>
<tr>
<td> Backstab </td><td> Parry </td><td> Summon </td>
</tr>
<tr>
<td> Shade Thrust </td><td> Warcry </td><td> Cure </td>
</tr>
</table>

###Starter attributes for character classes:
<table border=3px>
<tr>
<td>   </td><td> <b>Rogue</b>  </td><td> <b>Warrior</b>  </td><td> <b>Mage</b>  </td>
</tr>
<tr>
<td> Hp  </td><td> 22 </td><td> 25 </td><td> 19 </td>
</tr>
<tr>
<td> Sp  </td><td> 13 </td><td> 10 </td><td> 16 </td>
</tr>
<tr>
<td> Atk  </td><td> 10 </td><td> 15 </td><td> 5 </td>
</tr>
<tr>
<td> Def  </td><td> 5 </td><td> 15 </td><td> 10 </td>
</tr>
<tr>
<td> Ma  </td><td> 10 </td><td> 5 </td><td> 15 </td>
</tr>
<tr>
<td> Md  </td><td> 5 </td><td> 10 </td><td> 15 </td>
</tr>
<tr>
<td> Lck  </td><td> 15 </td><td> 5 </td><td> 5 </td>
</tr>
<tr>
<td> Spe  </td><td> 15 </td><td> 10 </td><td> 10 </td>
</tr>
</table>

####Abbreviations are defined as follows:
* Hp - Health
* Sp - Spill Points
* Atk - Attack
* Def - Defence
* Ma - Magical attack
* Md - Magical defence
* Lck - Luck
* Spe - Speed

###Deadline for this project varries.
