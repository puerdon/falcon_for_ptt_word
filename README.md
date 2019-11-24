# falcon_for_ptt_word
用來查詢ptt各版當中詞彙於各年份的頻率

- Step 1: build docker image
`$ docker-compose up --build`

- Step 2: 將各版的json複製到`board_data`資料夾
    <版名>.json
    json 格式:
    ```
    {
        "2004" <str: 年份>: {
            "打" <str: lemma>: {
                "NN" <str: pos>: 70 <int: freq>,
                "Va" <str: pos>: 100 <int: freq>,
                ...
            },
            ...
        },
        ...
    }
    ```
