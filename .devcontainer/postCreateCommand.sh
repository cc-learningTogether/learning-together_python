echo "hello world!"

git config --global user.email 'svartkatt39@gmail.com'
git config --global user.name 'miku0129'

mkdir -p ~/.ssh/
curl -s -o ~/.ssh/id_ed25519 "https://github.com/$(git config --global --get user.name).keys"