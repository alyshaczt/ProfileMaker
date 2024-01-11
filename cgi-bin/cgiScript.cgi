#!/usr/bin/perl 
use CGI ':standard';
use CGI::Carp qw ( fatalsToBrowser ); 
use File::Basename;
print "Content-type: text/html\n\n";
$CGI::POST_MAX = 1024 * 5000; 


my $phone_valid = 0;
my $phone = param('phone');
if (defined $phone && $phone =~ /^\d{10}$/) {
    $phone_valid = 1;
} else {
    print "<p>Invalid phone number. Please enter a 10-digit numeric phone number.</p>";
}

my $postal_valid = 0;
my $postal = param('postal');
if (defined $postal && $postal =~ /^[A-Za-z]\d[A-Za-z] \d[A-Za-z]\d$/) {
    $postal_valid = 1;
} else {
    print "<p>Invalid postal code. Please enter a postal code in the format L0L 0L0.</p>";
}

my $email_valid = 0;
my $email = param('email');
if (defined $email && $email =~ /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/) {
   $email_valid = 1;
} else {
    print "<p>Invalid email address. Please enter an email address in the format coolbeans\@sumn.sumn.</p>";
}

my $safe_filename_characters = "a-zA-Z0-9_.-";
my $upload_dir = "/home/acezette/public_html/upload";
my $filename = param('photo');

if ( !$filename ) {
  print header ( );
  print "There was a problem uploading your photo (try a smaller file).";
  exit;
}

my ( $name, $path, $extension ) = fileparse ( $filename, '\..*' );
$filename = $name . $extension;
$filename =~ tr/ /_/;
$filename =~ s/[^$safe_filename_characters]//g;

if ( $filename =~ /^([$safe_filename_characters]+)$/ ) {
  $filename = $1;
} else {
  die "Filename contains invalid characters";
}

my $upload_filehandle = upload("photo");
open ( UPLOADFILE, ">$upload_dir/$filename" ) or die "$!"; 
binmode UPLOADFILE;
while ( <$upload_filehandle> ) { print UPLOADFILE; } close UPLOADFILE;





if ($phone_valid && $postal_valid && $email_valid) {

my $fname     = param('fname');
my $lname     = param('lname');
my $address   = param('address');
my $city      = param('city');
my $province  = param('province');


my $profile = <<"PROFILE";
$fname $lname
$phone
$email
$address, $city, $province, $postal
PROFILE



print <<HTML;
<html>
<head>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #ffecf2;
            margin: 20px;
            padding: 20px;
        }
        .profile-card {
            max-width: 500px;
            margin: 90px auto; 
            background-color: #fff;
            padding: 20px;
            border-radius: 5px;
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            font-size: large;
        }

    </style>
</head>
<body>
    <div class="profile-card">
        <div><img src='../upload/$filename' alt='Profile Image' style='border-radius: 50%; margin-bottom: 20px; height: 150px; width: 150px; border: 4px solid #ffc0d4;'></div>
        <h2> $fname\'s Profile</h2>
        <pre>$profile</pre>
    </div>
</body>
</html>
HTML
}

else {
print <<HTML;
<html>
<head>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #ffecf2;
            margin: 20px;
            padding: 20px;
        }
        p {
            color: #e75480;
            font-size: larger;
        }
    </style>
</head>
<body>
</body>
</html>
HTML
}
