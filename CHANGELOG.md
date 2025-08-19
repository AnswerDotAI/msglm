# Release notes

<!-- do not remove -->

## 0.0.12


### Bugs Squashed

- /pdf/ triggers pdf mode when it should not ([#14](https://github.com/AnswerDotAI/msglm/issues/14))


## 0.0.11

### New Features

- Add TTL support for Anthropic prompt caching ([#13](https://github.com/AnswerDotAI/msglm/pull/13)), thanks to [@radekosmulski](https://github.com/radekosmulski)


## 0.0.10

### New Features

- Add support for PDFs by url ([#11](https://github.com/AnswerDotAI/msglm/pull/11)), thanks to [@sarahpannn](https://github.com/sarahpannn)


## 0.0.9

### New Features

- Auto handle empty text parts ([#12](https://github.com/AnswerDotAI/msglm/issues/12))


## 0.0.8

### New Features

- Improve `find_block` in openai to handle more message types, including reasoning outputs ([#10](https://github.com/AnswerDotAI/msglm/issues/10))
- Move openai to responses API ([#9](https://github.com/AnswerDotAI/msglm/issues/9))


## 0.0.7

### New Features

- add anthropic citation support ([#7](https://github.com/AnswerDotAI/msglm/pull/7)), thanks to [@comhar](https://github.com/comhar)

### Bugs Squashed

- `mk_msgs_anthropic` fails if no msgs ([#8](https://github.com/AnswerDotAI/msglm/issues/8))


## 0.0.6

### New Features

- add support for using a single cache checkpoint ([#4](https://github.com/AnswerDotAI/msglm/pull/4)), thanks to [@bclavie](https://github.com/bclavie)


## 0.0.4

### New Features

- add pdf support for Claude ([#2](https://github.com/AnswerDotAI/msglm/pull/2)), thanks to [@comhar](https://github.com/comhar)
- convert `mk_msg` output to `AttrDict`

## 0.0.3

### New Features

- use simpler message format for text only messages 

## 0.0.2

### Bugs Squashed

- fix `mk_img` bug
- fix openai tool use bug

## 0.0.1

- Init version

