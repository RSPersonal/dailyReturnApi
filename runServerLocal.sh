#!/usr/bin/env bash
cd core || exit
uvicorn main:app --reload
