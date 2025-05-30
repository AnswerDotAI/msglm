"""Create messages for language models like Claude and OpenAI GPTs."""

# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_core.ipynb.

# %% auto 0
__all__ = ['mk_msg_openai', 'mk_msgs_openai', 'mk_msg', 'mk_msgs', 'Msg', 'AnthropicMsg', 'OpenAiMsg', 'mk_msg_anthropic',
           'mk_msgs_anthropic', 'mk_ant_doc']

# %% ../nbs/00_core.ipynb
import base64
import mimetypes
from collections import abc

from fastcore import imghdr
from fastcore.meta import delegates
from fastcore.utils import *

# %% ../nbs/00_core.ipynb
def _mk_img(data:bytes)->tuple:
    "Convert image bytes to a base64 encoded image"
    img = base64.b64encode(data).decode("utf-8")
    mtype = mimetypes.types_map["."+imghdr.what(None, h=data)]
    return img, mtype

# %% ../nbs/00_core.ipynb
def _is_img(data): return isinstance(data, bytes) and bool(imghdr.what(None, data))

# %% ../nbs/00_core.ipynb
def _is_pdf(data): return isinstance(data, bytes) and data.startswith(b'%PDF-')

# %% ../nbs/00_core.ipynb
def _mk_pdf(data:bytes)->str:
    "Convert pdf bytes to a base64 encoded pdf"
    return base64.standard_b64encode(data).decode("utf-8")

# %% ../nbs/00_core.ipynb
def mk_msg(content:Union[list,str], role:str="user", *args, api:str="openai", **kw)->dict:
    "Create an OpenAI/Anthropic compatible message."
    text_only = isinstance(content, str) or (isinstance(content, list) and len(content) == 1 and isinstance(content[0], str))
    m = OpenAiMsg if api == "openai" else AnthropicMsg
    msg = m()(role, content, text_only=text_only, **kw)
    return dict2obj(msg, list_func=list)

# %% ../nbs/00_core.ipynb
def mk_msgs(msgs: list, *args, api:str="openai", **kw) -> list:
    "Create a list of messages compatible with OpenAI/Anthropic."
    if isinstance(msgs, str): msgs = [msgs]
    return [mk_msg(o, ('user', 'assistant')[i % 2], *args, api=api, **kw) for i, o in enumerate(msgs)]

# %% ../nbs/00_core.ipynb
class Msg:
    "Helper class to create a message for the OpenAI and Anthropic APIs."
    sdk_obj_support=False # is an SDK object a valid message?
    def __call__(self, role:str, content:[list,str], text_only:bool=False, **kw)->dict:
        "Create an OpenAI/Anthropic compatible message with `role` and `content`."
        if self.sdk_obj_support and self.is_sdk_obj(content): return self.find_block(content)
        if hasattr(content, "content"): content, role = content.content, content.role
        content = self.find_block(content)
        if content is not None and not isinstance(content, list): content = [content]
        content = [self.mk_content(o, text_only=text_only) for o in content] if content else ''
        return dict(role=role, content=content[0] if text_only else content, **kw)

    def is_sdk_obj(self, r)-> bool:
        "Check if `r` is an SDK object."
        raise NotImplemented
        
    def find_block(self, r)->dict:
        "Find the message in `r`."
        raise NotImplemented

    def text_msg(self, s:str, text_only:bool=False, **kw):
        "Convert `s` to a text message"
        return s if text_only else {"type":"text", "text":s}

    def img_msg(self, *args, **kw)->dict:
        "Convert bytes to an image message"
        raise NotImplemented

    def pdf_msg(self, *args, **kw)->dict:
        "Convert bytes to a pdf message"
        raise NotImplemented
    
    def mk_content(self, content:[str, bytes], text_only:bool=False) -> dict:
        "Create the appropriate data structure based the content type."
        if isinstance(content, str): return self.text_msg(content, text_only=text_only)
        if _is_img(content): return self.img_msg(content)
        if _is_pdf(content): return self.pdf_msg(content)
        return content

# %% ../nbs/00_core.ipynb
class AnthropicMsg(Msg):
    sdk_obj_support=False
    def img_msg(self, data: bytes) -> dict:
        "Convert `data` to an image message"
        img, mtype = _mk_img(data)
        r = {"type": "base64", "media_type": mtype, "data":img}
        return {"type": "image", "source": r}

    def pdf_msg(self, data: bytes) -> dict:
        "Convert `data` to a pdf message"
        r = {"type": "base64", "media_type": "application/pdf", "data":_mk_pdf(data)}
        return {"type": "document", "source": r}
    
    def is_sdk_obj(self, r)-> bool:
        "Check if `r` is an SDK object."
        return isinstance(r, abc.Mapping)

    def find_block(self, r):
        "Find the message in `r`."
        return r.get('content', r) if self.is_sdk_obj(r) else r

# %% ../nbs/00_core.ipynb
class OpenAiMsg(Msg):
    sdk_obj_support=True
    def img_msg(self, data: bytes) -> dict:
        "Convert `data` to an image message"
        img, mtype = _mk_img(data)
        r = {"url": f"data:{mtype};base64,{img}"}
        return {"type": "image_url", "image_url": r}

    def is_sdk_obj(self, r)-> bool:
        "Check if `r` is an SDK object."
        return type(r).__module__ != "builtins"

    def find_block(self, r):
        "Find the message in `r`."
        if not self.is_sdk_obj(r): return r
        m = nested_idx(r, "choices", 0)
        if not m: return m
        if hasattr(m, "message"): return m.message
        return m.delta

# %% ../nbs/00_core.ipynb
mk_msg_openai = partial(mk_msg, api="openai")
mk_msgs_openai = partial(mk_msgs, api="openai")

# %% ../nbs/00_core.ipynb
def _add_cache_control(msg, cache=False):
    "cache `msg`."
    if not cache: return msg
    if isinstance(msg["content"], str): msg["content"] = [{"type": "text", "text": msg["content"]}]
    if isinstance(msg["content"][-1], dict): msg["content"][-1]["cache_control"] = {"type": "ephemeral"}
    elif isinstance(msg["content"][-1], abc.Mapping): msg["content"][-1].cache_control = {"type": "ephemeral"}
    return msg

def _remove_cache_ckpts(msg):
    "remove unecessary cache checkpoints."
    if isinstance(msg["content"], str): msg["content"] = [{"type": "text", "text": msg["content"]}]
    elif isinstance(msg["content"][-1], dict): msg["content"][-1].pop('cache_control', None)
    else: delattr(msg["content"][-1], 'cache_control') if hasattr(msg["content"][-1], 'cache_control') else None
    return msg


@delegates(mk_msg)
def mk_msg_anthropic(*args, cache=False, **kwargs):
    "Create an Anthropic compatible message."
    msg = partial(mk_msg, api="anthropic")(*args, **kwargs)
    return _add_cache_control(msg, cache=cache)

@delegates(mk_msgs)
def mk_msgs_anthropic(*args, cache=False, cache_last_ckpt_only=False, **kwargs):
    "Create a list of Anthropic compatible messages."
    msgs = partial(mk_msgs, api="anthropic")(*args, **kwargs)
    if cache_last_ckpt_only: msgs = [_remove_cache_ckpts(m) for m in msgs]
    if not msgs: return msgs
    msgs[-1] = _add_cache_control(msgs[-1], cache=cache)
    return msgs

# %% ../nbs/00_core.ipynb
def mk_ant_doc(content, title=None, context=None, citation=True, **kws):
    "Create an Anthropic document."
    if _is_pdf(content): src = {"type":"base64", "media_type":"application/pdf", "data":_mk_pdf(content)}
    elif isinstance(content,list): src = {"type":"content", "content":content}
    else: src = {"type":"text", "media_type":"text/plain", "data":content}
    return {"type":"document", "source":src, "citations":{"enabled":citation}, "title":title, "context":context, **kws}
