function svn
{
  # Supported svn actions
  ACTIONS="add|checkout|co|cp|del|diff|export|merge|mkdir|move|mv|remove|rm|ren|st|sw|up"

  if [[ "$1" =~ ^($ACTIONS) ]]
  then
    eval $(which svn) "$@" | while IFS= read -r RL
    do
      if   [[ $RL =~ ^Index:\ |^@@|^= ]];  then C="\e[38;5;38m";           # File Name          = Blue
      elif [[ $RL =~ ^- ]];                then C="\e[38;5;1m";            # Removed            = Red
      elif [[ $RL =~ ^\+ ]];               then C="\e[38;5;2m";            # Added              = Green
      elif [[ $RL =~ ^\ ?M|^\ ?U ]];       then C="\e[38;5;38m";           # Modified/Updated   = Blue
      elif [[ $RL =~ ^\ ?C|^E ]];          then C="\e[48;5;1m\e[38;5;7m";  # Conflicted/Existed = Red Alert
      elif [[ $RL =~ ^A ]];                then C="\e[38;5;2m";            # Added              = Green
      elif [[ $RL =~ ^D ]];                then C="\e[38;5;1m";            # Deleted            = Red
      elif [[ $RL =~ ^! ]];                then C="\e[48;5;94m\e[38;5;7m"; # Item Missing       = Amber Alert
      elif [[ $RL =~ ^R|^G ]];             then C="\e[38;5;5m";            # Replaced or Merged = Purple
      elif [[ $RL =~ ^\? ]];               then C="\e[38;5;242m";          # No Version Control = Light Grey
      elif [[ $RL =~ ^I|^X|^Performing ]]; then C="\e[38;5;236m";          # Ignored            = Dark Grey
      else C=
      fi

      echo -e "$C${RL/\\/\\\\}\e[0m\e[0;0m"                                # Background and Text Reset
    done
  else
    eval $(which svn) "$@"
  fi
}
