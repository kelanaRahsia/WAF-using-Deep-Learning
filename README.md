# WAF-using-Deep-Learning
Integrating Deep Learning Model into Web Application Firewall to detect malicious behavior on Application Layer

This project is actually for my Final Year Project(FYP). The Deep Learning algorithm that is used in this project is LSTM(Long Short Term Memory).
I used LSTM because according to my research, it has the best accuracy for this type of scenario. This WAF is specifically trained to detect **SQLi**, **XSS** and **Command Injection**. 

Before start, you need to install CUDA, you can follow the youtube tutorial here: [https://youtu.be/39AV57Gqctc ](https://youtu.be/39AV57Gqctc) .
I run this Project on my **Ubuntu OS** and you also need GPU that support CUDA in order to run this code locally. If you do not have it, you can use Google Colab instead. Please make sure that you download the CUDA version that same with your GPU model.

You also need to setup MySQL server as the database of this project. I used XAMPP as the Web Server Solution Stack Package.

The Demonstration Website will be like this:

<img src="https://github.com/kelanaRahsia/WAF-using-Deep-Learning/assets/137630479/ebdfe67d-c369-444e-9f24-3e6f10a8674f" alt="image" width="80%" height="auto">

**The credential of this demo website is stated in the SQL file.**

After you successfully run all the code provided, you will be able to see another webpage.

<img src="https://github.com/kelanaRahsia/WAF-using-Deep-Learning/assets/137630479/0cca12b2-9276-491a-ad25-5e49e3d57d21" alt="image" width="80%" height="auto">

If you try to submit some malicious payload, an alert will appear according to the payload that you inserted.

<img src="https://github.com/kelanaRahsia/WAF-using-Deep-Learning/assets/137630479/3d902700-5bc0-47ce-9a32-af78864bf5b5" alt="image" width="50%" height="auto">


<h2>REMAINDER:</h2>
**You may encounter some error when you run this code, because of my CUDA version is not same with yours.**


