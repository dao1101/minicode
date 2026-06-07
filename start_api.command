#!/usr/bin/env zsh

base_dir="$(cd "$(dirname "$0")" && pwd)"

echo "======================================"
echo "         一键启动前后端项目"
echo "======================================"
echo
echo "按 Enter 继续..." && read -r

cd "$base_dir/backend"
minicode
