# WAF-using-Deep-Learning
Integrating Deep Learning Model into Web Application Firewall to detect malicious behavior on Application Layer

This project is actually for my Final Year Project(FYP). The Deep Learning algorithm that is used in this project is LSTM(Long Short Term Memory).
I used LSTM because according to my research, it has the best accuracy for this type of scenario. This WAF is specifically trained to detect **SQLi**, **XSS** and **Command Injection**. 

Before start, you need to install CUDA, you can follow the youtube tutorial here: [https://youtu.be/39AV57Gqctc ](https://youtu.be/39AV57Gqctc) .
I run this Project on my **Ubuntu OS** and you also need GPU that support CUDA in order to run this code locally. If you do not have it, you can use Google Colab instead. Please make sure that you download the CUDA version that same with your GPU model.

You also need to setup MySQL server as the database of this project. I used XAMPP as the Web Server Solution Stack Package.

The Demonstration Website will be like this:
![image](https://github.com/kelanaRahsia/WAF-using-Deep-Learning/assets/137630479/ebdfe67d-c369-444e-9f24-3e6f10a8674f)

The credential of stated in the SQL file.


