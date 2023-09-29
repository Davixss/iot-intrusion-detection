<?php

header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json; charset=UTF-8");

$emails = htmlentities($_GET['receivers'], ENT_QUOTES);
$subject = htmlentities($_GET['subject'], ENT_QUOTES);
$body = htmlentities($_GET['body'], ENT_QUOTES);

if(isset($emails) and isset($subject) and isset($body))
{
	$decodedSubject = html_entity_decode($subject, ENT_QUOTES);
	$decodedBody = html_entity_decode($body, ENT_QUOTES);

    $headers = "From: IoT-Notification \r\n";
    $headers .= "MIME-Version: 1.0\r\n";
    $headers .= 'Content-type: text/html; charset=iso-8859-1' . "\r\n";
    $headers .= "Content-Type: text/html; charset=UTF-8\r\n";

    $receivers = array();
    $emailList = explode(',', $emails);

    // Salvo nell'array receivers l'elenco delle emails
    foreach($emailList as $email)
    {
        $receivers[] = trim($email);
    }

    $n = 0;
    foreach($receivers as $receiver)
    {
        // Invio una email per ogni email dentro l'array receivers
        if(mail($receiver, $decodedSubject, $decodedBody, $headers))
        {
            $n++;
        }
        sleep(1);
    }

    http_response_code(200);
    echo json_encode("Success: $n emails sent");
}
else
{
    http_response_code(500);
    echo json_encode("Error: need all data to send emails");
}

?>