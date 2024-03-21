CDN_BASEURL = "https://cdn.signal.org/"

CDN_STICKER_URL_BASE = CDN_BASEURL + "stickers/{pack_id}/"
CDN_MANIFEST_URL = CDN_STICKER_URL_BASE + "manifest.proto"
CDN_STICKER_URL = CDN_STICKER_URL_BASE + "full/{sticker_id}"

SERVICE_BASEURL = "https://chat.signal.org"
SERVICE_STICKER_FORM_URL = SERVICE_BASEURL + "/v1/sticker/pack/form/{nb_stickers}"
