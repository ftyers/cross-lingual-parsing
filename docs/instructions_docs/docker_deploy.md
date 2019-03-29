# How to deploy docker container?

1. Clone repository

```bash
git clone https://github.com/maryszmary/hseling-web-universal-dependencies/
cd hseling-web-universal-dependencies
```
2. Checkout branch

```bash
git checkout front-mst
```
3. Build

```bash
docker build . -t web_ud
```
4. Run

```bash
docker run -p 5316:5316 --name web_ud_dev web_ud
```

5. Go to ```http://localhost:5316/``` in the browser
