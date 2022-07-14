# FEMZO
# Description
A Women Safety Based Web Application,  which helps women in handling all kinds of unsafe situations.
# Features
This Application helps users get to know of how to tackle abuses and assaults which happened to them physically or through cyber attacks.The Users can register in the website without revealing their identity to the organizations that run for the security of women.

# Api Used:
- ### Coin Market Cap 
    - to get list of all the Cryptos ( https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest )
    - to get details of a particular crypto using its symbol ( https://pro-api.coinmarketcap.com/v1/cryptocurrency/info?symbol=btc )
- ### CryptoCompare
    -to get news related to cryptos ( https://min-api.cryptocompare.com/data/news/ )

# Technology Used:
- It is built using The DJANGO FRAMEWORK which uses Python language.
- ### MVT Architecture
    - Django is based on MVT (Model-View-Template) architecture. MVT is a software design pattern for developing a web application. It is a Python-based web framework which allows you to quickly create web application without all of the installation or dependency problems that you normally will find with other frameworks.
    - MVT Structure has the following three parts :
        - Model: Model is going to act as the interface of your data. It is responsible for maintaining data. It is the logical data structure behind the entire application and is represented by a database (generally relational databases such as MySql, Postgres).
        - View: The View is the user interface — what you see in your browser when you render a website. It is represented by HTML/CSS/Javascript and Jinja files.
        - ViewModel: A template consists of static parts of the desired HTML output as well as some special syntax describing how dynamic content will be inserted.
     ![alt text](!https://media.geeksforgeeks.org/wp-content/uploads/20210606092225/image.png)

- ### Libraries for fetching data from Apis
    - #### Retrofit
        - Retrofit 2 is type-safe REST client build by square for Android and Java which intends to make it simpler to expand RESTful webservices. Retrofit 2 use OkHttp as the systems administration layer and is based over it. Retrofit naturally serializes the JSON reaction utilizing a POJO (PlainOldJavaObject).
        - need to add these lines inside dependencies{}: compile'com.google.code.gson:gson:2.6.2' , compile'com.squareup.retrofit2:retrofit:2.0.2', compile'com.squareup.retrofit2:converter-gson:2.0.2'
    - #### Volley
        - Volley is an HTTP library that makes networking very easy and fast, for Android apps. It was developed by Google and introduced during Google I/O 2013. It was developed because there is an absence in Android SDK, of a networking class capable of working without interfering with the user experience.
        -  Open build.gradle(Module: app) and add the following dependency: implementation 'com.android.volley:volley:1.0.0'

 
