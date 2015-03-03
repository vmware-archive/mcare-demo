//
//  RootViewController.m
//  mCare
//
//  Created by Bob Webster on 12/14/14.
//  Copyright (c) 2014 vca. All rights reserved.
//


#import "CustomerViewController.h"
#import "FavoritesList.h"
#import "User.h"
#import "Customer.h"
#import "TicketViewController.h"
#import "Builder.h"
#import "AppDelegate.h"
#import "LoginViewController.h"


#define kTitleFontSize 20.
#define kTitleFont [UIFont systemFontOfSize:kTitleFontSize]
#define kBgQueue dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0)


@interface CustomerViewController()

@property (copy, nonatomic) NSArray *customers;
//@property (weak, nonatomic) IBOutlet NSString *userId;
@property (weak, nonatomic) NSString *restUrl;

@end



@implementation CustomerViewController  

// called once
- (void)viewDidLoad {
    [super viewDidLoad];
    
    AppDelegate *appdelegate = (AppDelegate *)[UIApplication sharedApplication].delegate;
  
    _restUrl = [NSString stringWithFormat:@"%@/%@/", appdelegate.flaskUrl, @"api"];

  
    _customers = appdelegate.user.customers;
    
    // Hide the back button so the user cannot back into login page
  //  [self.navigationItem setHidesBackButton:YES animated:YES];

    // Make the rest call to lookup user id by name, will be async
    // example  localhost:5000/api/user?q{"filters":[{"name":"uname","op":"ge","val":"bob"}]}
     
  //  NSMutableString *searchString = [NSMutableString stringWithFormat:_restUrl];
  //  [searchString appendString:@"customer?q"];
 //   NSMutableString *sQuery = [NSMutableString stringWithFormat:@"filters\":[{\"name\":\"user_id\",\"op\":\"eq\",\"val\":\""];
 //   [sQuery appendString: appdelegate.user.uname];
 //   [sQuery appendString: @"\""];
 //   NSString *encodedUrl = [sQuery stringByAddingPercentEncodingWithAllowedCharacters:[NSCharacterSet URLHostAllowedCharacterSet]];
  //  [searchString appendString: encodedUrl];
  //  NSURL *searchUrl = [NSURL URLWithString:searchString];
    
  //  NSLog(@"Performing Rest call: %@, %@ ", searchString, sQuery );
    
    
    // Make the rest call on a background thread
    
  //  dispatch_async(kBgQueue, ^{
  //      NSData* data = [NSData dataWithContentsOfURL:searchUrl];
  //     [self performSelectorOnMainThread:@selector(fetchedData:) withObject:data waitUntilDone:YES];   });
    
    }



//- (void) fetchedData:(NSData *) responseData {
    // parse out the json data

    
    //debug line
 //   NSString *strData = [[NSString alloc]initWithData:responseData encoding:NSUTF8StringEncoding];
 //   NSLog(@"data=  %@", strData);
    
    
  //  NSError* jsonError;
  
 //   _customers = [Builder customersFromJSON:responseData error:&jsonError];

    
    // fix slow refresh of reloadData  not shown until scroll
 //   dispatch_async(dispatch_get_main_queue(), ^{
 //       [self.tableView reloadData];
  //  });
  
//}


#pragma mark - Table view data source

- (NSInteger)numberOfSectionsInTableView:(UITableView *)tableView {

        return 1;
}

- (NSInteger)tableView:(UITableView *)tableView numberOfRowsInSection:(NSInteger)section {
    // Return the number of rows in the section.
    NSLog(@"numberOfRowsTableView call on %@", tableView);

    NSLog(@"Number of Customers %lu", (unsigned long)[_customers count]);
  //  if([_customers count] == 0)
  //          return 1;
   //     else
             return [_customers count];
 
}



- (UITableViewCell *)tableView:(UITableView *)tableView
         cellForRowAtIndexPath:(NSIndexPath *)indexPath {

    static NSString *CustomerNameCell = @"CustomerName";
    UITableViewCell *cell = nil;
    

    NSLog(@"cellForRowAtIndexPath called on %@", tableView);
    
    // Configure the cell...
    
    cell = [tableView dequeueReusableCellWithIdentifier:CustomerNameCell
                                               forIndexPath:indexPath];
    
   
    Customer* customer = ((Customer *) _customers[indexPath.row]);
    cell.font = kTitleFont;
    cell.textAlignment = NSTextAlignmentCenter;
    cell.backgroundColor = [UIColor clearColor];
    cell.textLabel.text = customer.cname;
  
   
    if ([customer.opentickets integerValue] > 0)
        cell.detailTextLabel.text = [NSString stringWithFormat:@"%@", customer.opentickets];
    else
        cell.detailTextLabel.text = @"";
    
    UILabel *nameLabel = (UILabel *)[cell viewWithTag:100];
    nameLabel.font = [UIFont boldSystemFontOfSize:10.0];
   
    NSMutableString *address = [NSMutableString stringWithFormat:customer.street];
    [address appendString:@","];
    [address appendString:customer.city];
    [address appendString:@","];
    [address appendString:customer.state];
    
    nameLabel.text = address;
    
    return cell;
}

#pragma mark - Navigation

- (void)prepareForSegue:(UIStoryboardSegue *)segue sender:(id)sender {
    // Get the new view controller using [segue destinationViewController].
    // Pass the selected object to the new view controller.
    
    NSIndexPath *indexPath = [self.tableView indexPathForCell:sender];
    
     NSString *selCustomerId = [_customers[indexPath.row] id];
    
   
    NSString *selCustomerName = [_customers[indexPath.row] cname];
    
  //  [segue.destinationViewController navigationItem].title = @"Tickets";
    
    if ([segue.identifier isEqualToString:@"GetCustomerTickets"]) {
        TicketViewController *ticketsVC = segue.destinationViewController;
        ticketsVC.currentCustomerId = selCustomerId;
        ticketsVC.currentCustomerName = selCustomerName;
        [segue.destinationViewController navigationItem].title = @"Tickets";
    }
}


- (IBAction)logoutPressed:(id)sender {
    
   }
- (IBAction)logout:(id)sender {
    
    UIStoryboard* storyboard = [UIStoryboard storyboardWithName:@"Main" bundle:nil];
    LoginViewController *add =
    [storyboard instantiateViewControllerWithIdentifier:@"Login"];
    
    [self presentViewController:add
                       animated:YES
                     completion:nil];

}
@end
