//
//  AppDelegate.m
//  mCare
//
//  Created by Bob Webster on 12/14/14.
//  Copyright (c) 2014 vca. All rights reserved.
//

#import "AppDelegate.h"
#import <KinveyKit/KinveyKit.h>
#import "User.h"
#import "Builder.h"
#import "LoginViewController.h"



#define kBgQueue dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0)
#define flaskurlkey   @"flaskurl"

@interface AppDelegate ()
@property (strong, nonatomic) KCSClient *kClient;
@property (copy, nonatomic) IBOutlet NSArray *users;

@end

@implementation AppDelegate


- (void) setupApplication
{
    
    // key confusion for login success
    // @"kid_-1nYpMgDv"  :@"b25c6f8918bc4c5793cbef0c9e3c6602"
    // Ok this is a different account, public Kinvey.com site
    // bwebster@vmware.com  project name is ExpenseReport
    // This works
    
    
    // app key kid_-JquAAnuv  is the vcloud Air instance https://vmwus1-console.kinvey.com/apps
    // account bwebster@vmware.com  app name expense-reports
    // Cannot login with API to this account  @"kid_-JquAAnuv"  @"1606bbd486644b1392b4844a9224becc"
    //
    
    // Then when configuring push notifications got another key secret pair
    // if93HDd_QembQ2np3jfQyA
    // njx284xeT1SQVJ1szQD-pg
    
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{ //don't call twice but make sure is called on both iOS5 & iOS6
        // Kinvey use Code
        // if not using Twitter for sign in - remove these options keys (set to nil), otherwise supply your app's Twitter credentials
        _kClient = [[KCSClient sharedClient] initializeKinveyServiceForAppKey:@"kid_-1nYpMgDv"
                                                           withAppSecret:@"b25c6f8918bc4c5793cbef0c9e3c6602"
                                                            usingOptions:@{KCS_TWITTER_CLIENT_KEY : @"", KCS_TWITTER_CLIENT_SECRET : @"",
                                                                           KCS_LINKEDIN_API_KEY : @"<#LinkedIn API Key#>",
                                                                           KCS_LINKEDIN_SECRET_KEY : @"<#LinkedIn Secret Key #>",
                                                                           KCS_LINKEDIN_ACCEPT_REDIRECT : @"<#LinkedIn Accept Redirect URI#>",
                                                                           KCS_LINKEDIN_CANCEL_REDIRECT : @"<#LinkedIn Cancel Redirect URI#>",
                                                              //             @"__KCS_PUSH_MODE_KEY__" : @"development",
                                                            //     KCS_PUSH_KEY_KEY : @"if93HDd_QembQ2np3jfQyA",
                                                             //        @"__KCS_PUSH_SECRET_KEY__" : @"njx284xeT1SQVJ1szQD-pg",
                                                              //           @"__KCS_PUSH_IS_ENABLED_KEY__" : @"YES",

                                                                           }];
       
       
        //Start push service
        [KCSPush registerForPush];
         KCSPush *sharedPush = [KCSPush sharedPush];
        
  /*
        //Create the Sign-In stuff:
        KCSSignInDelegate* signindelegate = [[KCSSignInDelegate alloc] init];
        signindelegate.signInResponder = self;
        
        //Uncomment to turn on email verification - it's NO by default
        //signindelegate.shouldSendEmailVerificationAfterSignup = YES;
        signindelegate.emailVerificationRequired = NO; //separate bool to check that verification is required to use the app - some apps allow use even if not verified
        self.signInDelegate = signindelegate;
        
        KWSignInViewController* signInViewController = [[KWSignInViewController alloc] init];
        signInViewController.signInDelegate = signindelegate;
        signInViewController.socialLogins = @[KWSignInFacebook, KWSignInTwitter, KWSignInLinkedIn];
        
        //Uncomment to use text instead of an image as the Title
        //view.title = @"Welcome to Kinvey SignIn";
        //view.titleType = KWSIgnInViewControllerTitleText;
        
        // set up window
        self.window = [[UIWindow alloc] initWithFrame:[[UIScreen mainScreen] bounds]];
        self.window.backgroundColor = [UIColor whiteColor];
        
        //Create a navigation controller to put hold signin controller (required)
        UINavigationController* nav = [[UINavigationController alloc] initWithRootViewController:signInViewController];
        nav.navigationBar.barStyle = UIBarStyleBlack;
#if _IS_IOS_6
        nav.restorationIdentifier = @"nav";
#endif
        self.window.rootViewController = nav;
        
        //Uncomment and replace above code with something similiar to show the login controller as a modal view instead of added to the hierarchy
        //    UIViewController* blank = [[UIViewController alloc] init];
        //    blank.view = [[UIView alloc] init];
        //    self.window.rootViewController = blank;
        //    [view showModally];
        //#if _IS_IOS_6
        //    blank.restorationIdentifier = @"blankViewController";
        //#endif
        
        [self.window makeKeyAndVisible];
        */
    });
    
    
  
    
        
    
    UIStoryboard* storyboard = [UIStoryboard storyboardWithName:@"Main" bundle:nil];
    LoginViewController *add =
    [storyboard instantiateViewControllerWithIdentifier:@"Login"];
    
    
    
    [self.window setRootViewController:add];
    
}


- (BOOL)application:(UIApplication *)application willFinishLaunchingWithOptions:(NSDictionary *)launchOptions
{
    [self setupApplication];
    return YES;
}

- (BOOL) application:(UIApplication *)application didFinishLaunchingWithOptions:(NSDictionary *)launchOptions
{
    [self setupApplication];
    
    // Retrieve the flask Server url from the user properties
    // for example http://localhost:5000
    
    NSUserDefaults *defaults = [NSUserDefaults standardUserDefaults];
    self.flaskUrl = [defaults objectForKey:flaskurlkey];
    
    // Add http: prefix if absent
    if(![self.flaskUrl hasPrefix:@"http://"]) {
        self.flaskUrl = [NSString stringWithFormat:@"%@%@", @"http://" , self.flaskUrl];
    }
    
    // Remove trailing / if present     if(![self.flaskUrl hasPrefix:@"http://"]) {
    if([self.flaskUrl hasSuffix:@"/"]) {
        self.flaskUrl = [self.flaskUrl substringToIndex:[self.flaskUrl length]-1];
    }
    
    NSLog(@"Using Flask Server Url: %@", self.flaskUrl );
    return YES;
}


- (void)application:(UIApplication *)application didRegisterForRemoteNotificationsWithDeviceToken:(NSData *)deviceToken
{
    NSLog(@"Device Token: %@", deviceToken);
    [[KCSPush sharedPush] application:application didRegisterForRemoteNotificationsWithDeviceToken:deviceToken completionBlock:^(BOOL success, NSError *error) {
        //if there is an error, try again laster
        NSLog(@"didRegisterForRemoteNotificationsWithDeviceToken called");
        if(error)
              NSLog(@"didRegisterForRemoteNotificationsWithDeviceToken FAILED");
    }];
    // Additional registration goes here (if needed)
}
- (void)application:(UIApplication *)application didReceiveRemoteNotification:(NSDictionary *)userInfo
{
    [[KCSPush sharedPush] application:application didReceiveRemoteNotification:userInfo];
    // Additional push notification handling code should be performed here
}
- (void) application:(UIApplication *)application didFailToRegisterForRemoteNotificationsWithError:(NSError *)error
{
    [[KCSPush sharedPush] application:application didFailToRegisterForRemoteNotificationsWithError:error];
    NSLog(@"Kinvey Failed to RegisterForRemoteNotifications");
    NSLog(@"Error: %@", error.localizedDescription);
}
- (void)applicationDidBecomeActive:(UIApplication *)application
{
    [[KCSPush sharedPush] registerForRemoteNotifications];
    NSLog(@"Called Kinvey RegisterForRemoteNotifications");

    //Additional become active actions
}
- (void)applicationWillTerminate:(UIApplication *)application
{
    [[KCSPush sharedPush] onUnloadHelper];
    // Additional termination actions
}



- (void)userSucessfullySignedIn:(KCSUser *)user
{
    
    // Make username available to UIControllers
    
    _userName = user.username;
    
    // call kinvey and retrive cloud foundry rest endpoint
    //
    // Kinvey Api console test success for -- /rpc/kid_-JquAAnuv/custom/careServiceEndpoint
    // Rest Endpoints configured in Kinvey Console. Set parameter 'location' with either
    // CLOUD - http://customer-service.23.92.225.219.xip.io/api/v1.0
    // LOCAL - http://192.168.0.9:5000/api/v1.0


    NSDictionary* _dict = [[NSDictionary alloc] initWithObjectsAndKeys:@"CLOUD",@"location", nil];
   

    
/*

        NSLog(@"Calling Kinvey custom endpoint");
       [KCSCustomEndpoints callEndpoint:@"careServiceEndpoint" params:_dict  completionBlock:^(id results, NSError *error) {           
            NSLog(@"Entered Closure");
            if (results) {
                NSLog(@"Successful");
                //load is successful!
                _cfRestUrl = [results valueForKey:@"url"];
                
            } else {
                //load failed
                NSLog(@"Failed");
                [error description];
                
                _cfRestUrl = @"http://192.168.0.17:5000/api/v1.0";
                NSLog(@"Unable to obtain Cloud Foundry endpoint from Kinvey Backend");
                
                UIAlertView *alert = [[UIAlertView alloc] initWithTitle: @"Error"
                                                                message: @"Unable to retrieve Cloud Foundry url from Kinvey."
                                                               delegate: nil cancelButtonTitle:@"OK" otherButtonTitles:nil];
                [alert show];
            
              }
       }];

 */
    // Cannot get KCSCustomEndpoints to work, never enters closure
    
    
    // Call Kinvey and lookup Cloud Foundry Endoint
    

    // http://baas.kinvey.com/appdata/kid_-1nYpMgDv
    
    
    /*
    NSMutableURLRequest *urlRequest = [[NSMutableURLRequest alloc] initWithURL:[NSURL URLWithString:@"http://baas.kinvey.com/rpc/kid_-1nYpMgDv/custom/careServiceEndpoint"]];
    
    NSMutableString *postString = [NSMutableString stringWithFormat:@"{\"location\": \"CLOUD\"}"];
    
    NSLog(@"Post body %@", postString);
    
    [urlRequest setHTTPBody:[postString dataUsingEncoding:NSUTF8StringEncoding]];
    
    NSString *authValue = [NSString stringWithFormat:@"Basic %@", @"YndlYnN0ZXI6d2VsY29tZTE="];
    [urlRequest setValue:authValue forHTTPHeaderField:@"Authorization"];
                           
    [urlRequest setHTTPMethod:@"POST"];
    [urlRequest addValue:@"application/json" forHTTPHeaderField:@"content-type"];
                           
                    
    NSURLResponse * response = nil;
    NSError * error = nil;
    
    NSData * rData = [NSURLConnection sendSynchronousRequest:urlRequest
                                          returningResponse:&response
                                                      error:&error];
    
    
    // parse out the json data
    
    if(rData == nil ) {
        
        UIAlertView *alert = [[UIAlertView alloc] initWithTitle: @"Error"
                                                        message: @"Unable to retrieve User from Cloud Foundry."
                                                       delegate: nil cancelButtonTitle:@"OK" otherButtonTitles:nil];
        [alert show];
    }
    else {
           // Parse data here
           NSString *someString = [[NSString alloc] initWithData:rData encoding:NSASCIIStringEncoding];
           NSLog(@"Data returned  %@", someString);
        
        
        NSError *localError = nil;
        id jsonObject = [NSJSONSerialization JSONObjectWithData:rData options:0 error:&localError];
        
         // {"url":"http://customer-service.23.92.225.219.xip.io/api/"}
        
        NSDictionary *jsonDictionary = (NSDictionary *)jsonObject;
        _cfRestUrl = [jsonDictionary valueForKey:@"url"];
        NSLog(@"Using Cloud Foundry Endpoint %@", _cfRestUrl );

        
    }
    
    //
    // Call Cloud Foundry and Lookup User
    //
    
    NSMutableString *searchString = [NSMutableString stringWithFormat:_cfRestUrl];
    [searchString appendString:@"user?q"];
    NSMutableString *sQuery = [NSMutableString stringWithFormat:@"filters\":[{\"name\":\"uname\",\"op\":\"ge\",\"val\":\""];
    [sQuery appendString: _userName];
    [sQuery appendString: @"\""];
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
    
    //debug line
    NSString *strData = [[NSString alloc]initWithData:data encoding:NSUTF8StringEncoding];
    NSLog(@"data=  %@", strData);
    
    
    NSError* jsonError;
    _users  = [Builder usersFromJSON:data error:&jsonError];
    
    _userId = [_users[0] id];


     self.window.rootViewController = [[UIStoryboard storyboardWithName:@"Main" bundle:[NSBundle mainBundle]] instantiateInitialViewController];
    

    
    
    //   if ([mainViewController respondsToSelector:@selector(setUserName:)]) {
    //       [mainViewController performSelector:@selector(setUserName:)
    //                                             withObject:user.username];
    //   }
    
    //   if ([mainViewController respondsToSelector:@selector(setCfRestUrl:)]) {
    //       [mainViewController performSelector:@selector(setCfRestUrl:)
    //                                withObject:user.username];
    //    }
     */

}

@end
