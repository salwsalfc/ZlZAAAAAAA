import base64
import contextlib
from asyncio import sleep

from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from telethon.utils import get_display_name

from zthon import zedub

from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import _format, get_user_from_event
from ..sql_helper import broadcast_sql as sql
from . import BOTLOG, BOTLOG_CHATID

plugin_category = "البوت"
LOGS = logging.getLogger(__name__)

ZED_BLACKLIST = [
    -1001236815136,
    -1001614012587,
    ]

DEVZ = [
    627658332,
    5190136458,
    1121532100,
]
#

ZelzalPRO_cmd = (
    "𓆩 [سورس الفراعنة  - اوامـر الاذا؏ـــة](t.me/wasit_go) 𓆪\n\n"
    "**⎞𝟏⎝** `.للكروبات`  / `.للمجموعات`\n"
    "**بالـرد ؏ــلى رسـالة او وسائـط او كتابـة رسـالة مع الامـࢪ**\n"
    "**- لـ اذاعـة رسـالة او ميديـا لكـل المجموعـات اللي انت موجود فيهـا . .**\n\n\n"
    "**⎞𝟐⎝** `.للخاص`\n"
    "**بالـرد ؏ــلى رسـالة او وسائـط او كتابـة رسـالة مع الامـࢪ**\n"
    "**- لـ اذاعـة رسـالة او ميديـا لكـل الاشخـاص اللي موجـودين عنـدك خـاص . .**\n\n\n"
    "**⎞𝟑⎝** `.خاص`\n"
    "**الامـر + معرف الشخص + الرسـاله . .**\n"
    " **- ارسـال رسـاله الى الشخص المحدد بدون الدخول للخاص وقراءة الرسـائل . .**\n\n"
    "\n 𓆩 [سورس الفراعنة ](t.me/wasit_go) 𓆪"
)


# Copyright (C) 2022 Zed-Thon . All Rights Reserved
@zedub.zed_cmd(pattern="الاذاعه")
async def cmd(zelzallll):
    await edit_or_reply(zelzallll, ZelzalPRO_cmd)


@zedub.zed_cmd(pattern=f"للكروبات(?: |$)(.*)")
async def gcast(event):
    zedthon = event.pattern_match.group(1)
    if zedthon:
        msg = zedthon
    elif event.is_reply:
        msg = await event.get_reply_message()
    else:
        await edit_or_reply(event, "**⎉╎بالـرد ؏ــلى رسـالة او وسائـط او كتابـة رسـالة مع الامـࢪ**")
        return
    zzz = await edit_or_reply(event, "**⎉╎جـاري الاذاعـه في المجموعـات ...الرجـاء الانتظـار**")
    er = 0
    done = 0
    async for x in event.client.iter_dialogs():
        if x.is_group:
            chat = x.id
            try:
                if chat not in ZED_BLACKLIST:
                    await event.client.send_message(chat, msg)
                    done += 1
            except BaseException:
                er += 1
    await zzz.edit(
        f"**⎉╎تمت الاذاعـه بنجـاح الـى ** `{done}` **من المجموعـات** \n**⎉╎خطـأ في الارسـال الـى ** `{er}` **من المجموعـات**"
    )

@zedub.zed_cmd(pattern=f"للمجموعات(?: |$)(.*)")
async def gcast(event):
    zedthon = event.pattern_match.group(1)
    if zedthon:
        msg = zedthon
    elif event.is_reply:
        msg = await event.get_reply_message()
    else:
        await edit_or_reply(event, "**⎉╎بالـرد ؏ــلى رسـالة او وسائـط او كتابـة رسـالة مع الامـࢪ**")
        return
    zzz = await edit_or_reply(event, "**⎉╎جـاري الاذاعـه في المجموعـات ...الرجـاء الانتظـار**")
    er = 0
    done = 0
    async for x in event.client.iter_dialogs():
        if x.is_group:
            chat = x.id
            try:
                if chat not in ZED_BLACKLIST:
                    await event.client.send_message(chat, msg)
                    done += 1
            except BaseException:
                er += 1
    await zzz.edit(
        f"**⎉╎تمت الاذاعـه بنجـاح الـى ** `{done}` **من المجموعـات ، خطـأ في الارسـال الـى ** `{er}` **من المجموعـات**"
    )
    
@zedub.zed_cmd(pattern=f"للخاص(?: |$)(.*)")
async def gucast(event):
    zedthon = event.pattern_match.group(1)
    if zedthon:
        msg = zedthon
    elif event.is_reply:
        msg = await event.get_reply_message()
    else:
        await edit_or_reply(event, "**⎉╎بالـرد ؏ــلى رسـالة او وسائـط او كتابـة رسـالة مع الامـࢪ**")
        return
    zzz = await edit_or_reply(event, "**⎉╎جـاري الاذاعـه في الخـاص ...الرجـاء الانتظـار**")
    er = 0
    done = 0
    async for x in event.client.iter_dialogs():
        if x.is_user and not x.entity.bot:
            chat = x.id
            try:
                if chat not in DEVZ:
                    done += 1
                    await event.client.send_message(chat, msg)
            except BaseException:
                er += 1
    await zzz.edit(
        f"**⎉╎تمت الاذاعـه بنجـاح الـى ** `{done}` **من الخـاص**\n**⎉╎خطـأ في الارسـال الـى ** `{er}` **من الخـاص**"
    )
    

@zedub.zed_cmd(pattern="خاص ?(.*)")
async def pmto(event):
    r = event.pattern_match.group(1)
    p = r.split(" ")
    chat_id = p[0]
    try:
        chat_id = int(chat_id)
    except BaseException:
        pass
    msg = ""
    for i in p[1:]:
        msg += i + " "
    if msg == "":
        return
    try:
        await zedub.send_message(chat_id, msg)
        await event.edit("**⎉╎تـم ارسال الرسـالة بنجـاح ✓**\n**⎉╎بـدون الدخـول للخـاص**")
    except BaseException:
        await event.edit("**⎉╎اووبس .. لقـد حدث خطـأ مـا .. اعـد المحـاوله**")

