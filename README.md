# 概要
シフト提出、編集、閲覧をスマホから簡単に行えるWebアプリです。  
http://shiftmanagementapp.com  
  
- トップページは今月のシフトがひと目で確認できるカレンダー仕様
![スクリーンショット 2022-05-23 22 19 45](https://user-images.githubusercontent.com/66234583/169828627-0a3dbe51-1366-47b6-90d1-c879243eb278.png)  
  
- 日付クリックで非同期でシフトをサーバーに送信
![スクリーンショット 2022-05-23 22 17 46](https://user-images.githubusercontent.com/66234583/169828931-9b50eb76-82c1-4fe0-ad03-82edeca34d52.png)  
  
- 特定の日のシフト確認はわかりやすいタイムラインを使用
![スクリーンショット 2022-05-23 22 18 20](https://user-images.githubusercontent.com/66234583/169828999-808f107d-e428-4fc6-b665-2b2036b0b669.png)  
# 使用技術
**フロントエンド**
- jQuery 3.4.1
- Bootstrap 4.3.1
- GoogleCharts
- FullCalender 5.10.2
- HTML/CSS
  
**バックエンド**
- Python 3.7.10
- Django 3.2.13
  
**インフラ**
- AWS
    - EC2,RDS,S3,SES,Route53

![Untitled Diagram drawio-3](https://user-images.githubusercontent.com/66234583/167246404-5c10f21c-5aaf-4b73-a249-9cefec10d226.svg)