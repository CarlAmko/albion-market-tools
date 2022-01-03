#!/usr/bin/env python3
import subprocess


def run(spider: str, args: dict):
	cmd = f'scrapy crawl {spider}'
	for arg, val in args.items():
		cmd += f' -a {arg}={val}'

	subprocess.run(cmd, shell=True)
