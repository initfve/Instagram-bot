# Instagram bot

### Simple bot for Instagram with few options.<br>
    1. Show difference between following and followers
    2. Show top 10 the most active accounts on your or given account
    3. Like photos from hashtag


#### Usage
##### Check main account

`b = Bot("username", "password")` <br><br>
`1. b.showDiffBtwFollowingAndFollowers()`<br>
`2. b.showActiveUsers()`<br>
`3. b.likePhotosFromTag(tag="tag_name", limit=60, max=30))`

You can add bot.py to Cron or Windows Scheduler and automate e.g. like process
### Check other account
`b.changeWorkingAccount("username")`
 
### TODO
- [ ] Extended error handling




