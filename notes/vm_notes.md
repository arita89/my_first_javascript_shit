Connecting to a virtual machine (VM) via the Visual Studio Code (VS Code)using SSH (Secure Shell)

 **Install the Remote - SSH Extension**:
   - Open VS Code.
   - Go to the Extensions 
   - Search for "Remote - SSH" and click install on the extension by Microsoft.

**Set Up SSH Keys** (if necessary):
   - you’ll need to generate an SSH key pair on your local machine and add the public key to the VM.
   - (use git bash) to check on your current keys, this command will show you all the files in your .ssh directory. Common filenames include:

id_rsa (private key)
id_rsa.pub (public key)
id_ecdsa, id_ecdsa.pub
id_ed25519, id_ed25519.pub
```
ls -al ~/.ssh
```

- or to check your configuration file:
```
cat ~/.ssh/config
```

   - If you dont have any already usable ssh ket or you want a new one, with a unique name, you can generate keys using `ssh-keygen` in your local terminal.
```
ssh-keygen -t rsa -b 4096 -f ~/.ssh/my_custom_key
```
** Add the public key to your VM’s authorized keys** (if necessary):
(this step might be done in the background for you the first time you log in and a psw is asked, or not)
   - Check auth keys on the vm
```
nano ~/.ssh/authorized_keys
```
   - see public key from local
```
cat ~/.ssh/id_rsa.pub
```

   - copy public key from local, on Windows, if you're using Git Bash
```
cat ~/.ssh/id_rsa.pub | clip
```
   - copy public key from local, if on a Linux system with X11
```
cat ~/.ssh/id_rsa.pub | xclip -selection clipboard
```
- change permissions to the key making sure they are set to 600
```
chmod 600 ~/.ssh/authorized_keys
```


**Connect to Your VM**:
   - Open the Command Palette in VS Code with `Ctrl+Shift+P`.
   - Type "Remote-SSH: Connect to Host..." and press Enter.
   - Enter the SSH connection command in the format `username@hostname`, where `username` is your username on the VM and `hostname` is the IP address or URL of the VM.

**Open the VS Code Terminal**:
   - Once connected, you can open a new terminal in VS Code, which will now be connected to your VM.
   - Use the terminal as you would with a local terminal.

**Work on Your VM**:
   - You can now edit files, run commands, and use your VM directly through VS Code.
