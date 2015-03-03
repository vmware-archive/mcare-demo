//
//  CommentViewController.m
//  mCare
//
//  Created by Bob Webster on 12/29/14.
//  Copyright (c) 2014 vca. All rights reserved.
//

#import "CommentViewController.h"
#import "AppDelegate.h"
#import "Builder.h"
#import "User.h"

#define kBgQueue dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0)

@interface CommentViewController ()
- (IBAction)doneEntry:(id)sender;
@property (weak, nonatomic) IBOutlet UITextView *commentField;
@property (strong, nonatomic) IBOutlet NSString *restUrl;
@property (strong, nonatomic)  User *user;


@end

@implementation CommentViewController

// called once
- (void)viewDidLoad {
    [super viewDidLoad];
    // Do any additional setup after loading the view.
    
    AppDelegate *appdelegate = (AppDelegate *)[UIApplication sharedApplication].delegate;
    _restUrl = [NSString stringWithFormat:@"%@/%@/", appdelegate.flaskUrl, @"api/v1.0"];
    _user = appdelegate.user;
    
}

- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

- (IBAction)textFieldDoneEditing:(id)sender {
    [sender resignFirstResponder];
    
}

/*
#pragma mark - Navigation

// In a storyboard-based application, you will often want to do a little preparation before navigation
- (void)prepareForSegue:(UIStoryboardSegue *)segue sender:(id)sender {
    // Get the new view controller using [segue destinationViewController].
    // Pass the selected object to the new view controller.
}
*/

- (IBAction)doneEntry:(id)sender {
    NSLog(@"New Comment");
          //commentField.text
    
    
    NSDate *currentDate = [[NSDate alloc] init];
    
    NSTimeZone *timeZone = [NSTimeZone defaultTimeZone];
    // or specifc Timezone: with name
    
    NSDateFormatter *dateFormatter = [[NSDateFormatter alloc] init];
    [dateFormatter setDateFormat:@"yyyy-MM-dd HH:mm:ss.SSS"];
    NSString *localDateString = [dateFormatter stringFromDate:currentDate];
    
    NSMutableString *searchString = [NSMutableString stringWithFormat:_restUrl];
    [searchString appendString:@"comments"];
    
    NSURL *searchUrl = [NSURL URLWithString:searchString];

    NSURL *aUrl = [NSURL URLWithString:searchString];
    NSMutableURLRequest *request = [NSMutableURLRequest requestWithURL:aUrl
                                                           cachePolicy:NSURLRequestUseProtocolCachePolicy
                                                       timeoutInterval:10.0];
    
    [request setHTTPMethod:@"POST"];
    [request addValue:@"application/json" forHTTPHeaderField:@"content-type"];
    
   
    NSString *comment = [_commentField.text stringByReplacingOccurrencesOfString:@"\""
                                         withString:@"\'"];
    comment = [comment stringByReplacingOccurrencesOfString:@"\n"
                                                                      withString:@" "];
    
    // example
    //   NSString *postString = @"{\"body\": \"This is an even newer test comment\", \"timestamp\" : localDateString , \"notification\" : \"\", \"ticket_id\" : \"5\", \"user_id\" : \"1\"}";
    
    NSMutableString *postString = [NSMutableString stringWithFormat:@"{\"body\": \""];
    [postString appendString:comment];
    [postString appendString:@"\", \"timestamp\" : \""];
    [postString appendString:localDateString];
    [postString appendString:@"\", \"notification\" : \"\", \"ticket_id\" : \""];
    [postString appendString:_ticket.id];
    [postString appendString:@"\", \"user_id\" : \""];
    [postString appendString:_user.id];
    
    [postString appendString:@"\", \"email\" : \""];
    [postString appendString:_user.email];
    
    [postString appendString:@"\"}"];
    
    NSLog(@"Post body %@", postString);
    
    [request setHTTPBody:[postString dataUsingEncoding:NSUTF8StringEncoding]];
    
  //  UIAlertView *alert = [[UIAlertView alloc] initWithTitle: @"Debug"
  //                                                  message: postString
  //                                                 delegate: nil cancelButtonTitle:@"OK" otherButtonTitles:nil];
  //  [alert show];
    
    NSURLResponse * response = nil;
    NSError * error = nil;

    // Send a synchronous request

    NSData * data = [NSURLConnection sendSynchronousRequest:request
                                          returningResponse:&response
                                                      error:&error];
    
    if (error == nil)
    {
        // Parse data here
        NSString *someString = [[NSString alloc] initWithData:data encoding:NSASCIIStringEncoding];
        if (someString != nil && [someString length] > 0) {

            NSLog(@"Data returned  %@", someString);
        
            // Get the new comment returned
        
            NSError* jsonError;
            Comment *newComment  = [Builder commentFromJSON:data error:&jsonError];
        
            if(newComment == nil)
                NSLog(@"Builder Error processing Comment Query response: %@", [jsonError localizedDescription]);
            else {
            
                // Add to local datamodel
            
                [_ticket addComment:(newComment)];

            }
        }
        
        else {
                UIAlertView *alert = [[UIAlertView alloc] initWithTitle: @"Error"
                                                                message: @"Unable to retrieve Comment Data from Cloud Foundry."
                                                               delegate: nil cancelButtonTitle:@"OK" otherButtonTitles:nil];
                [alert show];
                
            }

             
    }
    
    
    NSLog(@"Added new Comment");
    
   

    // Pop the controller off the viewController stack

    [self.navigationController popViewControllerAnimated:YES];
}



- (void)touchesBegan:(NSSet *)touches withEvent:(UIEvent *)event {
    
    UITouch *touch = [[event allTouches] anyObject];
    if ([_commentField isFirstResponder] && [touch view] != _commentField) {
        [_commentField resignFirstResponder];
    }
    [super touchesBegan:touches withEvent:event];
}



@end
