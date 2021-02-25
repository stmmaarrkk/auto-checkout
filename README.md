Momo Helper
===
This is a program contains various helper functions for Momo.
---

### Features ###
<ul>
  <li> Automatically login.
  <li> Automatically fill out the checkout form.
  <li> Automatically refresh the page to check if there is an add-to-cart button and put that item into cart and perform checkout.
</ul>

### Demo video ###
[![](http://img.youtube.com/vi/byn7ik9PS28/0.jpg)](https://youtu.be/byn7ik9PS28 "Demo Video")

### Prerequisites ###
<ul>
  <li> MacOS, Chrome.
  <li> Python 3.7.3 or above
  <li> Bash
</ul>

### Quick start instructions
<ol type="1">
  <li> Clone the whole directory to your Mac.
  <li> Install Pyhon 3.7.3 or above
  <li> Open your command line use <code>cd</code> command go to the "auto_check" directory.
  <li> In the first time, use root user to execute <code>sudo ./setup</code> to build the executed environmentrun. (You don't have to run "setup" every time before launching "Momo_helper", run in the first time or some unexpected error happens)
  <li> Use normal user to execute <code>./Momo_helper</code> to run the program and follow the instructions.
</ol>

### Environments
OS: *MacOS, Catalina 10.15.7*   
chrome driver: *ChromeDriver 87.0.4280.88*  
python: *Python 3.7.3*
Shell: bash 3.2


### Updates
**2020/12/15**
<ul>
  <li> Add automatically generate user-agent. 
  <li> Auto download newest chrome driver.
  <li> Use excutable script start program.
</ul>

**2020/12/16**
<ul>
  <li> Perform downloading chrome driver at setup
  <li> Temporarily pause auto-login
</ul>

**2020/12/17**
<ul>
  <li> Add local cache to program browser to load page faster
  <li> Activate auto-login function
  <li> Add auto refresh and add-to-cart function
</ul>
