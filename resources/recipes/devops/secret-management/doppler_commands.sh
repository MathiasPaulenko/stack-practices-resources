#!/usr/bin/env bash
# Doppler CLI workflow: install, login, inject, export

brew install dopplerhq/doppler/doppler

doppler login
doppler setup

# Run app with secrets injected into the environment
doppler run -- npm start

# Export secrets to .env for CI pipelines
doppler secrets download --no-file --format=env > .env
