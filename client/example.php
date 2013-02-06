<?php

require('./socketclient.php');


print_r(exchange('example', 'hello', array('abc', 'def')));
                  //entry    //func  //args
