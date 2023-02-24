<h1 align="center"> Flet notion python </h1>

<p align="center"> <img width="40%" src="https://i.imgur.com/ackusnx.png"> </p>

✨ Inspiration from [Python Tutorial UI Design Using Flet - Line Indent](https://youtu.be/JJCjAUmNXBs)

I've attempted to implement Notion as a database, then use an api to connect to fetch data from Notion and display it on Flet, a Python-programmable flutter GUI module.

# Install

```
git clone https://github.com/watchakorn-18k/flet-notion-python
cd flet-notion-python
pip install -r requirements.txt
```

# Settings

- Add token from [notion.so/my-integrations](https://www.notion.so/my-integrations) then put to `token.json`

- Add table follow here

```
| income | client-name |
```

![](https://i.imgur.com/6gQ2anM.png)

```json
{
  "token": ""
}
```

# Run

```
flet ui.py
```

# Build

```
pyinstaller ui.space
```

This is merely an illustration of how to use notion's api with flet. You may attempt to fix a lot of mistakes. -- wk-18k 2023
