del yandex_function.zip

7z a ^
  yandex_function.zip ^
  requirements.txt ^
  handlers.py ^
  yandex_function.py ^
  yandex_logging.py ^
  .env ^
  -tzip

yc serverless function version create ^
  --function-name=silencer ^
  --runtime python312 ^
  --entrypoint yandex_function.yandex_function_handler ^
  --memory 128m ^
  --execution-timeout 5s ^
  --source-path ./yandex_function.zip

del yandex_function.zip
