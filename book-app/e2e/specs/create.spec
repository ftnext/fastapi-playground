# Bookを登録できる

## /booksにPOSTリクエストを送って、Bookを登録できる
* パス"/books"に
* メソッド"POST"で
* メディアタイプ"application/json"で
* JSON<file:fixtures/books/post/request.json>で
* リクエストを送る

* レスポンスのステータスコードが
* 整数値の"201"である
* DB"bookdb"にSQL"select isbn, title, page from book"を実行した結果が
* テーブル<table:fixtures/books/post/assertion.csv>である
