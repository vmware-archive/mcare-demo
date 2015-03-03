//
//  TicketInfoTableViewController.m
//  mCare
//
//  Created by Bob Webster on 12/20/14.
//  Copyright (c) 2014 vca. All rights reserved.
//

#import "TicketInfoViewController.h"
#import "Ticket.h"
#import "AppDelegate.h"
#import "Builder.h"
#import "CommentViewController.h"
#import "CommentTableViewCell.h"

#define kTitleFontSize 28.
#define kTitleFont [UIFont systemFontOfSize:kTitleFontSize]

#define kDetailFontSize 16.
#define kDetailFont [UIFont systemFontOfSize:kDetailFontSize]

#define kHeaderFontSize 10.
#define kHeaderFont [UIFont systemFontOfSize:kHeaderFontSize]

#define kBgQueue dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0)

@interface TicketInfoViewController()

@property (assign, nonatomic) CGFloat cellPointSize;
@property (strong, nonatomic) NSString *restUrl;
@property (copy, nonatomic) NSArray *tickets;
@property (copy, nonatomic) NSMutableArray *comments;

@end

@implementation TicketInfoViewController


- (void)viewDidLoad {
    [super viewDidLoad];
    
    AppDelegate *appdelegate = (AppDelegate *)[UIApplication sharedApplication].delegate;
    _restUrl = [NSString stringWithFormat:@"%@/%@/", appdelegate.flaskUrl, @"api/v1.0"];
    
        
    // if the _currentCustomerId is null then we are getting tickets for a specific customer
    
    NSMutableString *searchString = [NSMutableString stringWithFormat:_restUrl];
    
    
    if (_ticket == nil) {
        
        NSLog(@"Error: no ticket  passed to TicketInfoViewController");
    }
    else {
        [searchString appendString:@"tickets/"];
        [searchString appendString:_ticket.id];
        //     [searchString appendString:(@"/tickets")];
        
    }
    
    
    NSURL *searchUrl = [NSURL URLWithString:searchString];
    
    // Make the rest call on a background thread
    
    NSLog(@"Performing Rest call: %@ ", searchString);
    
    dispatch_async(kBgQueue, ^{
        NSData* data = [NSData dataWithContentsOfURL:searchUrl];
        [self performSelectorOnMainThread:@selector(fetchedData:) withObject:data waitUntilDone:YES];   });
    
    NSLog(@"Received ticket id %@",_ticket.id);
    
    self.tableView.estimatedRowHeight = 60.0;
    self.tableView.rowHeight = UITableViewAutomaticDimension;

}

- (UIView *)tableView:(UITableView *)tableView viewForHeaderInSection:(NSInteger)section {
    

    UIView* headerView = nil;

    if(section == 0) {

        headerView = [[UIView alloc] initWithFrame:CGRectMake(0, 0, tableView.frame.size.width, 22)];
        
        headerView.backgroundColor = [UIColor colorWithWhite:0.8f alpha:1.0f];
        headerView.layer.borderColor = [UIColor colorWithWhite:0.8 alpha:1.0].CGColor;
        headerView.layer.borderWidth = 1.0;
        
        UILabel* headerLabel = [[UILabel alloc] init];
        headerLabel.frame = CGRectMake(5, 2, tableView.frame.size.width - 5, 18);
        headerLabel.backgroundColor =[UIColor clearColor];
        //  headerLabel.textColor = [UIColor orangeColor];


        headerLabel.font = [UIFont boldSystemFontOfSize:16.0];
        headerLabel.text = [NSString stringWithFormat:@"%@ %@", @"Ticket: ", _ticket.tnumber];
        headerLabel.textAlignment = NSTextAlignmentLeft;
        [headerView addSubview:headerLabel];

    }
    else {
        
        static NSString *CellIdentifier = @"commentHeader";
        UITableViewCell *cell = [tableView dequeueReusableCellWithIdentifier:CellIdentifier];

        cell.backgroundColor = [UIColor colorWithWhite:0.8f alpha:1.0f];
        cell.layer.borderColor = [UIColor colorWithWhite:0.8 alpha:1.0].CGColor;
        cell.layer.borderWidth = 1.0;

        UILabel *nameLabel = (UILabel *)[cell viewWithTag:100];
        nameLabel.font = [UIFont boldSystemFontOfSize:16.0];
        nameLabel.text = @" Comments";
        
   //     nameLabel.text = [NSString stringWithFormat:@"%lu %@", (unsigned long)[_ticket.comments count], @"Comments"];
  //      headerLabel.textAlignment = NSTextAlignmentLeft;
        
 //       UIView *myView = [[UIView alloc] initWithFrame:CGRectMake(0.0, 0.0, 300.0, 20.0)];
    //    UIButton *button = [UIButton buttonWithType:UIButtonTypeContactAdd];
  //      [button setFrame:CGRectMake(275.0, 5.0, 30.0, 30.0)];
  //      button.tag = section;
   //     button.hidden = NO;
   //     [button setBackgroundColor:[UIColor clearColor]];
    //    [button addTarget:self action:@selector(insertParameter:) forControlEvents:UIControlEventTouchDown];
    //    [headerView addSubview:button];
    //    return myView;
        
        headerView = cell;
    }
    
                                                                
 //   [headerView addSubview:headerLabel];
    return headerView;
}

- (void)tableView:(UITableView *)tableView willDisplayHeaderView:(UIView *)view forSection:(NSInteger)section
{
    if([view isKindOfClass:[UITableViewHeaderFooterView class]]){
        
        UITableViewHeaderFooterView *tableViewHeaderFooterView = (UITableViewHeaderFooterView *) view;
        tableViewHeaderFooterView.textLabel.textColor = [UIColor blueColor];
    }
}

- (void)viewDidAppear:(BOOL)animated
{
    [super viewDidAppear:animated];
    [self.tableView reloadData];
}


- (void) fetchedData:(NSData *) responseData {
        // parse out the json data
    
    
    //debug line
     NSString *strData = [[NSString alloc]initWithData:responseData encoding:NSUTF8StringEncoding];
     NSLog(@"http returned data=  %@", strData);
    
    // Get the selected ticket
    NSError* jsonError;
    _tickets  = [Builder ticketsFromJSON:responseData error:&jsonError];
    
    if(_tickets == nil) {
       NSLog(@"Builder Error processing Query response: %@", [jsonError localizedDescription]);
    }
    else {
        _ticket = (Ticket*) _tickets[0];  // get the single ticket returned by this query
        NSLog(@"Builder returned %lu", (unsigned long)[_tickets count] );
        
    }

    
    // fix slow refresh of reloadData  not shown until scroll
    dispatch_async(dispatch_get_main_queue(), ^{
        [self.tableView reloadData];
    });
    
    
}



- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

#pragma mark - Table view data source

- (NSInteger)numberOfSectionsInTableView:(UITableView *)tableView {
    // Return the number of sections.
   
      return 2;
   }

- (NSInteger)tableView:(UITableView *)tableView numberOfRowsInSection:(NSInteger)section {
    // Return the number of rows in the section.
    NSLog(@"ticket %@ ",  self.ticket);
    if (section == 0) {
        return 1;
    } else {
       
        return [[self.ticket comments] count] ;
    }
}

- (NSString *)tableView:(UITableView *)tableView
titleForHeaderInSection:(NSInteger)section {
    if (section == 0) {
        return @"Ticket Detail";
    } else {
        return @"Comments";
    }
}


- (UITableViewCell *)tableView:(UITableView *)tableView
         cellForRowAtIndexPath:(NSIndexPath *)indexPath {
    static NSString *TicketDetailCell = @"ticketDetail";
    static NSString *CommentDetailCell = @"commentDetail";
    UITableViewCell *cell = nil;
    CommentTableViewCell *ccell = nil;
    
    // Configure the cell...
    if (indexPath.section == 0) {
        cell = [tableView dequeueReusableCellWithIdentifier:TicketDetailCell
                                               forIndexPath:indexPath];
        cell.textLabel.font = kDetailFont;
        cell.textLabel.text =  [self.ticket body];
        
        NSDateFormatter *dateFormatter = [[NSDateFormatter alloc] init];
        [dateFormatter setDateFormat:@"yyyy-MM-dd'T'HH:mm:ss"];
        NSDate *dateObj = [dateFormatter dateFromString:[self.ticket timestamp]];  // string to NSDate
        [dateFormatter setDateFormat:@"MM dd yyyy"];
        [dateFormatter setDateStyle:NSDateFormatterLongStyle]; // day, Full month and year
        [dateFormatter setTimeStyle:NSDateFormatterNoStyle];  // nothing
        NSString *localDateString = [dateFormatter stringFromDate:dateObj];

        cell.detailTextLabel.text = localDateString;
        cell.textLabel.numberOfLines = 0;
        cell.textLabel.lineBreakMode = NSLineBreakByWordWrapping;
        return cell;
        
    } else {
        ccell = [tableView dequeueReusableCellWithIdentifier:CommentDetailCell
                                               forIndexPath:indexPath];
        
        
        NSMutableArray* comments = [_ticket comments];
        NSLog(@"%lu comments", (unsigned long)[comments count]);
        
      
        Comment *comment = ((Comment *) comments[indexPath.row]);

        
        // Date and Who
     //   NSDateFormatter *dateFormatter = [[NSDateFormatter alloc] init];
     //   [dateFormatter setDateFormat:@"yyyy-MM-dd'T'HH:mm:ss"];
     //   NSDate *lDate = [dateFormatter dateFromString:comment.timestamp];
        
     //   [dateFormatter setDateFormat:@"MM dd yyyy"];
     //   [dateFormatter setDateStyle:NSDateFormatterLongStyle]; // day, Full month and year
      //  [dateFormatter setTimeStyle:NSDateFormatterNoStyle];  // nothing
     //   NSString *localDateString = [dateFormatter stringFromDate:lDate];
      //  ccell.headerLabel.text = localDateString;  //Date and Who
        ccell.headerLabel.text = comment.timestamp;  //Date and Who

        
        ccell.headerRightLabel.text = comment.email;  //Date and Who

        ccell.bodyLabel.numberOfLines = 10;
        ccell.bodyLabel.lineBreakMode = NSLineBreakByWordWrapping;
        ccell.bodyLabel.text = [NSString stringWithFormat:@"%@",((Comment *) comment.body)];
        return ccell;
        
    }
  }



// Override to support conditional editing of the table view.
- (BOOL)tableView:(UITableView *)tableView canEditRowAtIndexPath:(NSIndexPath *)indexPath {
    // Return NO if you do not want the specified item to be editable.
    if(indexPath.section == 0)
        return NO;
    else
        return YES;
}



// Override to support editing the table view.
- (void)tableView:(UITableView *)tableView commitEditingStyle:(UITableViewCellEditingStyle)editingStyle forRowAtIndexPath:(NSIndexPath *)indexPath {
    if (editingStyle == UITableViewCellEditingStyleDelete) {
       
        // Delete the row from the data source
        
        NSMutableString *searchString = [NSMutableString stringWithFormat:_restUrl];
        [searchString appendString:@"comments/"];
        
        
        NSMutableArray* comments = [_ticket comments];
        NSLog(@"%lu comments", (unsigned long)[comments count]);
        NSString* commentId = [NSString stringWithFormat:@"%@",((Comment *) comments[indexPath.row]).id];
        
        [_ticket removeComment:(commentId)];
       
      
        [searchString appendString:commentId];

        
        // Delete the comment from the server
        
        NSLog(@"Search String %@", searchString);
        
        
        NSURL *aUrl = [NSURL URLWithString:searchString];
        NSMutableURLRequest *request = [NSMutableURLRequest requestWithURL:aUrl
                                                               cachePolicy:NSURLRequestUseProtocolCachePolicy
                                                           timeoutInterval:10.0];
        
        [request setHTTPMethod:@"DELETE"];
        [request addValue:@"application/json" forHTTPHeaderField:@"content-type"];
        
        NSURLResponse * response = nil;
        NSError * error = nil;
        
        // Send a synchronous request
        
        NSData * data = [NSURLConnection sendSynchronousRequest:request
                                              returningResponse:&response
                                                          error:&error];
        
        if (error == nil)
        {
            // Parse data here
            NSLog(@"Data returned  %@", data);
        }
        
        
        NSLog(@"Deleted Comment");
        

        
        [tableView deleteRowsAtIndexPaths:@[indexPath] withRowAnimation:UITableViewRowAnimationFade];
        
    } else if (editingStyle == UITableViewCellEditingStyleInsert) {
        // Create a new instance of the appropriate class, insert it into the array, and add a new row to the table view
    }   
}


/*
// Override to support rearranging the table view.
- (void)tableView:(UITableView *)tableView moveRowAtIndexPath:(NSIndexPath *)fromIndexPath toIndexPath:(NSIndexPath *)toIndexPath {
}
*/

/*
// Override to support conditional rearranging of the table view.
- (BOOL)tableView:(UITableView *)tableView canMoveRowAtIndexPath:(NSIndexPath *)indexPath {
    // Return NO if you do not want the item to be re-orderable.
    return YES;
}
*/


#pragma mark - Navigation

// In a storyboard-based application, you will often want to do a little preparation before navigation
- (void)prepareForSegue:(UIStoryboardSegue *)segue sender:(id)sender {
    
 
 //  [segue.destinationViewController navigationItem].title = @"Tickets";
 
 if ([segue.identifier isEqualToString:@"newComment"]) {
 CommentViewController *newCommentVC = segue.destinationViewController;
 newCommentVC.ticket = self.ticket;
   
 }
 }

@end
