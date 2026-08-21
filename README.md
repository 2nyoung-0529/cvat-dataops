# CVAT DataOps

CVAT REST API를 활용하여 데이터 라벨링 프로젝트의 작업 현황을 자동으로 조회하고
진행률을 계산하는 간단한 DataOps 도구입니다.

## Why

데이터 라벨링 프로젝트를 운영하면서 작업량과 진행률을 수기로 집계하면
반복적인 확인 작업이 발생하고 집계 오류가 생길 수 있습니다.

CVAT에 이미 존재하는 작업 데이터를 API로 가져와
작업 현황을 자동으로 계산하는 것을 목표로 만들었습니다.

## Features

현재 v1에서는 다음 기능을 지원합니다.

- CVAT Task 자동 조회
- Task별 Job 자동 조회
- Job Annotation 조회
- 전체 이미지 수 계산
- 라벨링 완료 이미지 수 계산
- 미작업 이미지 수 계산
- Annotation 객체 수 계산
- 작업 진행률 자동 계산

## Example

테스트 데이터 기준:

```text
Task ID: 2529256
Name: shipyard_productivity_test

Total images: 10
Annotated images: 3
Unannotated images: 7
Annotation count: 6
Progress: 30.0%