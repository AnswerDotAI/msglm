# msglm


<!-- WARNING: THIS FILE WAS AUTOGENERATED! DO NOT EDIT! -->

### Installation

Install the latest version from pypi

``` sh
$ pip install msglm
```

## Usage

To use an LLM we need to structure our messages in a particular format.

Here’s an example of a text chat from the OpenAI docs.

``` python
from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
  model="gpt-4o",
  messages=[
    {"role": "user", "content": "What's the Wild Atlantic Way?"}
  ]
)
```

Generating the correct format for a particular API can get tedious. The
goal of *msglm* is to make it easier.

The examples below will show you how to use *msglm* for text and image
chats with OpenAI and Anthropic.

### Text Chats

For a text chat simply pass a list of strings and the api format
(e.g. “openai”) to **mk_msgs** and it will generate the correct format.

``` python
mk_msgs(["Hello, world!", "some assistant response"], api="openai")
```

``` js
[
    {"role": "user", "content": "Hello, world!"},
    {"role": "assistant", "content": "Some assistant response"}
]
```

#### anthropic

``` python
from msglm import mk_msgs_anthropic as mk_msgs
from anthropic import Anthropic
client = Anthropic()

r = client.messages.create(
    model="claude-3-haiku-20240307",
    max_tokens=1024,
    messages=[mk_msgs(["Hello, world!", "some LLM response"])]
)
print(r.content[0].text)
```

#### openai

``` python
from msglm import mk_msgs_openai as mk_msgs
from openai import OpenAI

client = OpenAI()
r = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[mk_msgs(["Hello, world!", "some LLM response"])]
)
print(r.choices[0].message.content)
```

### Image Chats

For an image chat simply pass the raw image bytes in a list with your
question to *mk_msgs* and it will generate the correct format.

``` python
mk_msg([img, "What's in this image?"], api="anthropic")
```

``` js
[
    {
        "role": "user", 
        "content": [
            {"type": "image", "source": {"type": "base64", "media_type": media_type, "data": img}}
            {"type": "text", "text": "What's in this image?"}
        ]
    }
]
```

#### anthropic

``` python
import httpx
from msglm import mk_msg_anthropic as mk_msg
from anthropic import Anthropic

client = Anthropic()

img_url = "https://www.atshq.org/wp-content/uploads/2022/07/shutterstock_1626122512.jpg"
img = httpx.get(img_url).content

r = client.messages.create(
    model="claude-3-haiku-20240307",
    max_tokens=1024,
    messages=[mk_msg([img, "Describe the image"])]
)
print(r.content[0].text)
```

#### openai

``` python
import httpx
from msglm import mk_msg_openai as mk_msg
from openai import OpenAI

img_url = "https://www.atshq.org/wp-content/uploads/2022/07/shutterstock_1626122512.jpg"
img = httpx.get(img_url).content

client = OpenAI()
r = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[mk_msg([img, "Describe the image"])]
)
print(r.choices[0].message.content)
```

### API Wrappers

To make life a little easier, msglm comes with api specific wrappers for
[`mk_msg`](https://AnswerDotAI.github.io/msglm/core.html#mk_msg) and
[`mk_msgs`](https://AnswerDotAI.github.io/msglm/core.html#mk_msgs).

For Anthropic use

``` python
from msglm import mk_msg_anthropic as mk_msg, mk_msgs_anthropic as mk_msgs
```

For OpenAI use

``` python
from msglm import mk_msg_openai as mk_msg, mk_msgs_openai as mk_msgs
```

### Other use-cases

#### Prompt Caching

*msglm* supports [prompt
caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)
for Anthropic models. Simply pass *cache=True* to *mk_msg* or *mk_msgs*.

``` python
from msglm import mk_msg_anthropic as mk_msg

mk_msg("please cache my message", cache=True)
```

This generates the expected cache block below

``` js
{
    "role": "user",
    "content": [
        {"type": "text", "text": "Please cache my message", "cache_control": {"type": "ephemeral"}}
    ]
}
```

#### PDF chats

*msglm* offers PDF
[support](https://docs.anthropic.com/en/docs/build-with-claude/pdf-support)
for Anthropic. Just like an image chat all you need to do is pass the
raw pdf bytes in a list with your question to *mk_msg* and it will
generate the correct format as shown in the example below.

``` python
import httpx
from msglm import mk_msg_anthropic as mk_msg
from anthropic import Anthropic

client = Anthropic(default_headers={'anthropic-beta': 'pdfs-2024-09-25'})

url = "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf"
pdf = httpx.get(url).content

r = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[mk_msg([pdf, "Which model has the highest human preference win rates across each use-case?"])]
)
print(r.content[0].text)
```

Note: this feature is currently in beta so you’ll need to:

- use the Anthropic beta client
  (e.g. `anthropic.Anthropic(default_headers={'anthropic-beta': 'pdfs-2024-09-25'})`)
- use the `claude-3-5-sonnet-20241022` model

### Summary

We hope *msglm* will make your life a little easier when chatting to
LLMs. To learn more about the package please read this
[doc](https://answerdotai.github.io/msglm/).