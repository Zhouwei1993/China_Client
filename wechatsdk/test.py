from wechatsdk import WC_SDK

wechat = WC_SDK.WechatQy(appid="wx3b49bdadb178a548", appsecret="DHApUxn4EvIqYN5zez1ew6rSIKupHR47RtIQOndoR2z9XOL8fMuf0zVWrB-iCh9n")
r = wechat.grant_token()
print(r)

