# 会議室予約アプリ

## 環境構築

```shell
docker compose up -d
```

- [APIドキュメント](http://localhost:8080/docs)
- [pgadmin](http://localhost:81)

## 修正が必要な内容

### リレーション関係

- BookingとUser、BookingとRoomはそれぞれ1対多の関係になっているが、本来は多対多であるべき

### 予約可能かの判断

- 予約した時間帯にすでに予約が入っているかどうかの判定ができていない
