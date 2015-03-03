//
//  LoginViewController.m
//  mCare
//
//  Created by Bob Webster on 12/16/14.
//  Copyright (c) 2014 vca. All rights reserved.
//

#import "LoginViewController.h"
#import <KinveyKit/KinveyKit.h>
#import "CustomerViewController.h"

#import "Builder.h"
#import "AppDelegate.h"
#import "User.h"

@interface LoginViewController ()

@property (weak, nonatomic) IBOutlet UIButton *loginButton;
@property (weak, nonatomic) IBOutlet UITextField *loginField;
@property (weak, nonatomic) IBOutlet UITextField *passwordField;
@property (copy, nonatomic) IBOutlet NSArray *users;
@property (weak, nonatomic) IBOutlet NSString *restUrl;


@end

@implementation LoginViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    // Do any additional setup after loading the view.
    
  
    
    AppDelegate *appdelegate = (AppDelegate *)[UIApplication sharedApplication].delegate;
    
  //  if(![appdelegate.flaskUrl containsString:@"http://"]) {
  //      NSLog(@"%@ ", @"Error: Unable to read valid flask server url");

  //      UIAlertView *alert = [[UIAlertView alloc] initWithTitle: @"Error"
   //                                                     message: @"Unable to retrieve User from Cloud Foundry."
                                                   //    delegate: nil cancelButtonTitle:@"OK" otherButtonTitles:nil];
    //    [alert show];
   // }
}



- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

- (IBAction)buttonPressed:(UIButton *)sender {
    
    AppDelegate *appdelegate = (AppDelegate *)[UIApplication sharedApplication].delegate;
    
    
    // @"http://customer-service.23.92.225.219.xip.io/api/";
    
    _restUrl = [NSString stringWithFormat:@"%@/%@/", appdelegate.flaskUrl, @"api/v1.0"];
    appdelegate.userName = _loginField.text;
    
    NSMutableString *authString = [NSMutableString stringWithFormat:appdelegate.flaskUrl];
    [authString appendString:(@"/loginauth")];
    
    NSInteger rc = [self authenticateUser:authString
                                  username:_loginField.text password:_passwordField.text];
    
    if(rc == 302)
    {
        User* userObj = [self lookupUser:_loginField.text endpoint:_restUrl];
        appdelegate.user= userObj;
        
        
        // Login to Kinvey
        
        [self kinveyLogin:userObj.kinveyuser password:userObj.kinveypassword];
        
        
        [self performSegueWithIdentifier:@"TabBar" sender:sender];
        
    } else {
        
        UIAlertView *alert = [[UIAlertView alloc] initWithTitle: @"Error"
                                                        message: @"Invalid Login."
                                                       delegate: nil cancelButtonTitle:@"OK" otherButtonTitles:nil];
        [alert show];

    }

}

- (IBAction) backgroundTap:(id) sender {
    [self.loginField resignFirstResponder];
    [self.passwordField resignFirstResponder];
}


// This will get called too before the view appears
- (void)prepareForSegue:(UIStoryboardSegue *)segue sender:(id)sender
{
    if ([[segue identifier] isEqualToString:@"GetCustomers"]) {
        
        
        if ([segue.destinationViewController respondsToSelector:@selector(setUserId:)]) {
            [segue.destinationViewController performSelector:@selector(setUserId:)
                                                  withObject:_userId];
        }
        
    }
}


- (IBAction)textFieldDoneEditing:(id)sender {
    [sender resignFirstResponder];

}


- (void)userSucessfullySignedIn:(KCSUser *)user
{
    NSLog(@"Login Successful");
}


- (User*) lookupUser:(NSString*) userName
                     endpoint:(NSString*) endpoint {
    
    //
    // Call Flask Server and Lookup User
    //
    
    // example http://192.168.0.12:5000/api/v1.0/users?q={"uname": "bwebster"}
    
    NSMutableString *searchString = [NSMutableString stringWithFormat:endpoint];
    [searchString appendString:@"users?q="];
    NSMutableString *sQuery = [NSMutableString stringWithFormat:@"{\"uname\": \""];
    [sQuery appendString: userName];
    [sQuery appendString: @"\"}"];
    NSString *encodedUrl = [sQuery stringByAddingPercentEncodingWithAllowedCharacters:[NSCharacterSet URLHostAllowedCharacterSet]];
    [searchString appendString: encodedUrl];
    NSURL *searchUrl = [NSURL URLWithString:searchString];
    
    NSLog(@"Performing Rest call: %@ ", searchUrl );
    
    
    // Make the rest call on a background thread
    
    //   dispatch_async(kBgQueue, ^{
    NSData* data = [NSData dataWithContentsOfURL:searchUrl];
    //      [self performSelectorOnMainThread:@selector(fetchedData:) withObject:data waitUntilDone:YES];   });
    
    // parse out the json data
    
    if(data == nil ) {
        
        UIAlertView *alert = [[UIAlertView alloc] initWithTitle: @"Error"
                                                        message: @"Unable to retrieve User from Cloud Foundry."
                                                       delegate: nil cancelButtonTitle:@"OK" otherButtonTitles:nil];
        [alert show];
    }
    else {
    
       //debug line
       NSString *strData = [[NSString alloc]initWithData:data encoding:NSUTF8StringEncoding];
       NSLog(@"data=  %@", strData);
    
    
       NSError* jsonError;
       _users  = [Builder usersFromJSON:data error:&jsonError];
    
      //  NSString *userId = [_users[0] id];
    }
    return _users[0];
}


- (NSInteger) authenticateUser:(NSString*) endpoint
                      username:(NSString*) username
                      password:(NSString*) password {
    
    NSMutableURLRequest *urlRequest = [[NSMutableURLRequest alloc] initWithURL:[NSURL URLWithString:endpoint]];
    
  //  NSMutableString *postString = [NSMutableString stringWithFormat:@"{\"location\": \"CLOUD\"}"];
    
 //   NSLog(@"Post body %@", postString);
    
 //   [urlRequest setHTTPBody:[postString dataUsingEncoding:NSUTF8StringEncoding]];
    
    NSMutableString *creds = [NSMutableString stringWithFormat:username];
    [creds appendString:@":"];
    [creds appendString:password];
    
    
    // Create NSData object
    NSData *nsdata = [creds
                      dataUsingEncoding:NSUTF8StringEncoding];
    
    // Get NSString from NSData object in Base64
    NSString *base64Encoded = [nsdata base64EncodedStringWithOptions:0];
    
    NSString *authValue = [NSString stringWithFormat:@"Basic %@", base64Encoded];
    [urlRequest setValue:authValue forHTTPHeaderField:@"Authorization"];
    
    [urlRequest setHTTPMethod:@"GET"];
    [urlRequest addValue:@"application/json" forHTTPHeaderField:@"content-type"];
    
    
    NSHTTPURLResponse * response = nil;
    NSError * error = nil;
   
    [NSURLConnection sendSynchronousRequest:urlRequest
                                           returningResponse:&response
                                                       error:&error];
    
     NSString* responseUrl =  [[response URL] absoluteString];
    
    if( [responseUrl containsString:(@"/login/")] )
        return 302;
    
    else return [response statusCode];
    
}


- (void) kinveyLogin:(NSString *) username password:(NSString *) password {
    
  
    
    [KCSUser loginWithUsername:username password:password withCompletionBlock:^(KCSUser *user, NSError *errorOrNil, KCSUserActionResult result) {
        if (errorOrNil == nil) {
            //the log-in was successful and the user is now the active user and credentials saved
            //hide log-in view and show main app content
            [self userSucessfullySignedIn:user];
 
        } else { //there was an error with the update save
            NSString* message = [errorOrNil localizedDescription];
            NSLog(@"%@ %@", @"Kinvey Login Error", message);
            UIAlertView* alert = [[UIAlertView alloc] initWithTitle:NSLocalizedString(@"Create account failed", @"Sign account failed")
                                                            message:message
                                                            delegate:nil
                                                            cancelButtonTitle:NSLocalizedString(@"OK", @"OK")
                                                            otherButtonTitles: nil];
            [alert show];
        }
    }];
    


     
  }

@end
