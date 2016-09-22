# Research Project in Communication

The purpose of this project is to collect Tweets mentioning a specific user.

## Requirements

This scrips contains in the folder **streaming_tweets** runs on Python2 because of the package `imagehash` and the folder named **database_management** runs on both Python version (2 and 3). You will need to install the requirements (dependencies) in order to run the scripts.
```
  pip install -r requirements.txt
```
Some files needs some credentials in order to run. `downloads.py` needs your Dropbox API credentials and your `email` credentials. This file also requires to create a `SQL like Database` and you must provide your connection credentials.


## Usage
```
  cd streaming_tweets
  python main.py
```



## Contributing

1. Fork it ( https://github.com/guinslym/comm_research_project/fork )
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create a new Pull Request
