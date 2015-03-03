//
//  TicketViewController.m
//  mCare
//
//  Created by Bob Webster on 12/15/14.
//  Copyright (c) 2014 vca. All rights reserved.
//

#import "TicketViewController.h"
#import "Customer.h"
#import "Builder.h"
#import "AppDelegate.h"
#import "TicketInfoViewController.h"
#import "Ticket.h"

#define kTitleFontSize 24.
#define kTitleFont [UIFont systemFontOfSize:kTitleFontSize]
#define kBgQueue dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0)

@interface TicketViewController()
@property (copy, nonatomic) NSArray *tickets;
@property (copy, nonatomic) NSArray *customers;
@property (assign, nonatomic) CGFloat cellPointSize;
@property (weak, nonatomic) IBOutlet NSString *restUrl;

@end

@implementation TicketViewController


- (void)viewDidLoad {
    [super viewDidLoad];
    
    AppDelegate *appdelegate = (AppDelegate *)[UIApplication sharedApplication].delegate;
    _restUrl = [NSString stringWithFormat:@"%@/%@/", appdelegate.flaskUrl, @"api/v1.0"];

    
    // Solution
    // cellForRowsAtIndexPath not called until way after call to  [self.tableView reloadData];
    // http://stackoverflow.com/questions/5349162/why-self-tableview-reloaddata-does-not-work
   // self.tableView.dataSource = self;  //this line

    // if the _currentCustomerId is null then we are getting tickets for a specific customer
   
    NSMutableString *searchString = [NSMutableString stringWithFormat:_restUrl];
    
    
    if (_currentCustomerId == nil) {
      
        [searchString appendString:@"tickets"];  // Currently No marshaller for this case
    }
        else {
               [searchString appendString:@"customers/"];
               [searchString appendString:_currentCustomerId];
          //     [searchString appendString:(@"/tickets")];
        }
    
    
    NSURL *searchUrl = [NSURL URLWithString:searchString];

    // Make the rest call on a background thread
    
    NSLog(@"Performing Rest call: %@ ", searchString);

    dispatch_async(kBgQueue, ^{
        NSData* data = [NSData dataWithContentsOfURL:searchUrl];
        [self performSelectorOnMainThread:@selector(fetchedData:) withObject:data waitUntilDone:YES];   });
    
    
}

- (void) fetchedData:(NSData *) responseData {
    // parse out the json data
    
    
    //debug line
    NSString *strData = [[NSString alloc]initWithData:responseData encoding:NSUTF8StringEncoding];
    
    if (strData != nil && [strData length] > 0) {
        
        
        NSLog(@"http returned data=  %@", strData);
    
        if (_currentCustomerId != nil) {
         
            // Get the selected customer
            NSError* jsonError;
            _customers  = [Builder customersFromJSON:responseData error:&jsonError];
    
            if(_customers == nil)
                NSLog(@"Builder Error processing Query response: %@", [jsonError localizedDescription]);
            else {
                _tickets = [_customers[0] tickets];  // get the tickets for the returned customer
                NSLog(@"Builder returned %lu", (unsigned long)[_tickets count] );
       }
        } else {
            // Get all tickets not related to customer
            NSError* jsonError;
            _tickets  = [Builder ticketsFromJSON:responseData error:&jsonError];
         
        }
    }
    else {
        UIAlertView *alert = [[UIAlertView alloc] initWithTitle: @"Error"
                                                        message: @"Unable to retrieve Ticket Data from Cloud Foundry."
                                                       delegate: nil cancelButtonTitle:@"OK" otherButtonTitles:nil];
        [alert show];
        _tickets = [[NSArray alloc] init];
        
    }

    
    // fix slow refresh of reloadData  not shown until scroll
    dispatch_async(dispatch_get_main_queue(), ^{
        [self.tableView reloadData];
    });

    
}


#pragma mark - Table view data source

- (NSInteger)numberOfSectionsInTableView:(UITableView *)tableView {
    NSLog(@" numberOfSectionsinTableView called on %@", tableView);
    return 1;
}

- (NSInteger)tableView:(UITableView *)tableView numberOfRowsInSection:(NSInteger)section {
    NSLog(@"numberOfRowsTableView call on %@", tableView);
    
  //  if(_tickets == nil)
  //      return 0;
 //   else
        return [_tickets count];
    
}

- (NSString *)tableView:(UITableView *)tableView
titleForHeaderInSection:(NSInteger)section {
   
    return _currentCustomerName;
  
}
    
- (UITableViewCell *)tableView:(UITableView *)tableView
cellForRowAtIndexPath:(NSIndexPath *)indexPath {
    static NSString *TicketCell = @"TicketName";
    UITableViewCell *cell = nil;
    
    
    NSLog(@"cellForRowAtIndexPath called on %@", tableView);
    
    // Configure the cell...
   
        cell = [tableView dequeueReusableCellWithIdentifier:TicketCell
                                               forIndexPath:indexPath];
        
       // font set in Storyboard
  //      cell.font = kTitleFont;
   //     cell.textAlignment = NSTextAlignmentCenter;
        cell.backgroundColor = [UIColor clearColor];
        Ticket* t =_tickets[indexPath.row];
        NSLog(@"%@", t);
    
        NSMutableString *tNumSummary = [NSMutableString stringWithFormat:@"%@",t.tnumber];
        [tNumSummary appendString:@"    "];
        [tNumSummary appendString:[NSString stringWithFormat:t.ttype]];

        cell.textLabel.text = tNumSummary;
    
        NSDateFormatter *dateFormatter = [[NSDateFormatter alloc] init];
    //    [dateFormatter setDateFormat:@"yyyy-MM-ddTHH:mm"];
        [dateFormatter setDateFormat:@"yyyy-MM-dd'T'HH:mm:ss"];
        NSDate *lDate = [dateFormatter dateFromString:t.timestamp];
    
        [dateFormatter setDateFormat:@"MM dd yyyy"];
        [dateFormatter setDateStyle:NSDateFormatterLongStyle]; // day, Full month and year
        [dateFormatter setTimeStyle:NSDateFormatterNoStyle];  // nothing
        NSString *localDateString = [dateFormatter stringFromDate:lDate];
    
        NSMutableString *typeAndTime = [NSMutableString stringWithFormat:@"%@",localDateString];
        [typeAndTime appendString:@"    "];
        [typeAndTime appendString:t.cemail];

    
    

        cell.detailTextLabel.text = typeAndTime;
    
    if([t.tstate  isEqual: @"OPEN"])
    {
        UIImage *image = [UIImage imageNamed:@"Circle_Red_16x16"];
       cell.imageView.image = image;
    }
        else {
    
            UIImage *image2 = [UIImage imageNamed:@"Circle_Grey_16x16"];
            cell.imageView.image = image2;
        }
    
    
    return cell;
}



#pragma mark - Navigation

- (void)prepareForSegue:(UIStoryboardSegue *)segue sender:(id)sender {
    // Get the new view controller using [segue destinationViewController].
    // Pass the selected object to the new view controller.
    
    NSIndexPath *indexPath = [self.tableView indexPathForCell:sender];
    
    
    [segue.destinationViewController navigationItem].title = @"Ticket Info";
    
    if ([segue.identifier isEqualToString:@"GetTicketInfo"]) {
        TicketInfoViewController *ticketInfoVC = segue.destinationViewController;
        Ticket* t =_tickets[indexPath.row];
     //   ticketInfoVC.ticketId =  t.id;
        ticketInfoVC.ticket = t;
    }
    
}















@end
