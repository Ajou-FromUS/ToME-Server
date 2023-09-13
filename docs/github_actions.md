# Github Actions

## 작업 환경

### 개발용 서버

- Working Directory
    ```
    /home/lifeteer/actions-runner/
    ```

- Github Actions YML Path
    ```
    /home/lifeteer/dev-main/.github/workflows/deploy.yml
    ```

- Managing Service

    - Starting Service
        ```
        /home/lifeteer/actions-runner/svc.sh start
        ```
    
    - Stopping Service
        ```
        /home/lifeteer/actions-runner/svc.sh stop
        ```

    - Service Status
        ```
        /home/lifeteer/actions-runner/svc.sh status
        ```

- Github Actions Setting
    ```
    https://github.com/Ajou-Lifeteer/Lifeteer-Server/settings/actions/runners
    ```

    - 위 URL에서 Runner로 등록된 서버의 작동 여부 확인 가능
    - 개발용 서버는 dev-main으로 Runner 이름을 지정

- Authority Issues

    - Actions Runner를 서비스에 등록하는 과정에서 sudo 관련 이슈들이 발생
    - sudo 유저와 lifeteer 유저와 함께 같이 lifeteer 그룹에 포함되도록 설정
    - working directory 하위 폴더에 해당 그룹에 대한 권한을 업데이트하여 sudo 유저가 디렉토리에 접근할 수 있도록 설정
    - 서비스가 제대로 작동하려면 /home/lifeteer/actions-runner/.credentials_rsaparams에 대하여 접근 가능해야 함.

- Basic Structure
    - Git과 연동되어있는 디렉토리에 ./.github/workflows/ 디렉토리를 만들고 해당 위치에 deploy.yml을 작성
    - 해당 yml에는 Github Actions 설정들이 명시되어 있고, Github Actions는 해당 yml을 기반으로 Github Actions Runner들에 Job을 할당
    - 현재 설정으로는 Main 브랜치에 Push가 발생할 경우, Github Actions가 작동하여 Runner로 등록해놓은 개발용 서버에서 특정 동작들을 하도록 되어있음