#!/usr/bin/env bash

#Function for Registration
register() {
 username=$1
 read -s -p "Create password: " password
 echo
 passwordhash=$(echo -n "$password" | sha256sum | awk '{print $1}')
 echo -e "${username}\t${passwordhash}" >> users.tsv
 echo "Registered successfully!"
}

#Function for Login
login() {
  user=$1
  until [[ "$user" =~ [a-zA-Z0-9]+$ ]]; do
    read -p "Please enter a valid username: " user
  done
  if ! grep -q "^${user}	" users.tsv; then
    read -p "This username does not exist. Do you want to register?(y/n)" reg
    while true; do
      if [[ "$reg" == "y" ]]; then
        register "${user}"
        break
      elif [[ "$reg" == "n" ]]; then
        echo "Registration unsuccessfull. Please start the game again."
        exit 0
      else
        echo "This is not a valid input. Please try again."
        read -p "Do you want to register?(y/n)" reg
      fi
    done
  else
    password_match="false"

    while [[ "$password_match" == "false" ]]; do
      read -s -p "Enter password: " password1
      echo
      password1_given=$(echo -n "$password1" | sha256sum | awk '{print $1}')
      password1_actual=$(grep "${user}	" users.tsv | cut -f 2)
      if [[ "$password1_actual" == "$password1_given" ]]; then 
        password_match=true
        echo "Login Successful."
      else 
        echo "Password incorrect! Please try again."
      fi
    done
  fi
}


# User-1 login:
read -p "Enter username: " username1
login "$username1"


# User-2 login:
read -p "Enter username: " username2
while [[ "$username1" == "$username2" ]]; do
  read -p "Please enter a different username: " username2
done
login "$username2"

#Start the game with the two authenticated users
python3 game.py "$username1" "$username2"

