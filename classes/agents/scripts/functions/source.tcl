
#############################################################################
proc message {status message} {
    set red_color "\033\[1;31m"
    set green_color "\033\[1;32m"
    set yellow_color "\033\[1;33m"
    set light_blue_color "\033\[1;36m"
    set no_color "\033\[0m"

    if {$status == "INFO"} {
        puts -nonewline $green_color;
    } elseif {$status == "WARNING"} {
        puts -nonewline $yellow_color;
    } elseif {$status == "HIGHLIGHT"} {
        puts -nonewline $light_blue_color;
    } elseif {$status == "NO_COLOR"} {
        puts -nonewline $no_color;
        return;
    } else {
        puts -nonewline $red_color;
    }
    puts $message
    puts -nonewline $no_color;
}


#############################################################################
# parse file:
# break a csv like file into a list of lists
proc parseFile {filename} {
    set data {}
    set fileId [open $filename r]
    while {[gets $fileId line] >= 0} {
        set parsedLine [split $line ";"]
        lappend data $parsedLine
    }
    close $fileId
    return $data
}

#############################################################################
#remove substring
#returns a string without a substring
proc removeSubstring {inputStr subStr} {
    if {[string first $subStr $inputStr] != -1} {
        set index [string first ":" $inputStr]
        if {$index != -1} {
            set prefix [string range $inputStr 0 [expr $index-1]]
            if {$prefix eq $subStr} {
                set result [string range $inputStr [expr $index+1] end]
                return $result
            }
        }
    }
    return ""
}

#############################################################################
#list from file
#receives a file and returns a list containing each line content
proc listFromFile {filename} {
    set f [open $filename r]
    set data [split [string trim [read $f]]]
    close $f
    return $data
}

#############################################################################
#list file to list
#reads a file and return a list, different than listFromFile
#readFileToList will keep the spaces on each file line
proc readFileToList {filename} {
    set data [list]
    set file [open $filename r]
    while {[gets $file line] != -1} {
        lappend data $line
    }
    close $file
    return $data
}

#############################################################################
#check if comment
#check if first char is #
proc isNotComment { line } {
    if {[string index $line 0] ne "#"} {
        return 1
    } else {
        return 0
    } 
}

#############################################################################
#exists
#check if file exists
proc lexists name {
    expr {![catch {file lstat $name finfo}]}
}

#############################################################################
#replace character
#replace one character for another in a string
proc replaceChar {str oldChar newChar} {
    return [string map [list $oldChar $newChar] $str]
}

#############################################################################
#ends with
#check if string ends with substring
proc endsWith {str subStr} {
    set strLen [string length $str]
    set subStrLen [string length $subStr]

    # Check if substring is longer than string
    if {$subStrLen > $strLen} {
        return false
    }

    # Extract the end portion of the original string of the same length as subStr
    set endOfStr [string range $str [expr {$strLen - $subStrLen}] end]

    # Compare the end portion and the substring
    if {[string equal $endOfStr $subStr]} {
        return true
    } else {
        return false
    }
}

#############################################################################
#is list empty?
#check if list is empty

proc isListEmpty {inputList} {
    if {[llength $inputList] == 0} {
        return 1 ;# List is empty
    } else {
        return 0 ;# List is not empty
    }
}

#############################################################################
#remove last substring
#given a path, returns everything before the char /
proc removeLastSubstring {path} {
    # Find the last index of '/'
    set last_slash_index [string last "/" $path]

    # Extract the substring up to the last '/'
    if {$last_slash_index != -1} {
       return [string range $path 0 $last_slash_index]
    } else {
       # If no '/' is found, return the original path
       return $path
    }
}

#############################################################################
#get unique
#return all the unique elements of a list
proc getUnique {list} {
    # Use dict to efficiently get unique values
    return lsort -unique $list
}

