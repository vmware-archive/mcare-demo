//
//  CustomerBuilder.m
//  mCare
//
//  Created by Bob Webster on 12/14/14.
//  Copyright (c) 2014 vca. All rights reserved.
//

//  Note: NSJSONSerialization, all the keyed lists are automatically turned into NSDictionary objects.
//  For array, it’s converted into NSArray instances. Any strings encountered along with the names of named items
//  in keyed lists are converted into NSString, while purely numeric strings are converted into NSNumber objects.
//  This can lead to surprising NSCFNumber exceptions later during assignment when a value thought of as a String
//  is parsed into a NSNumber

#import "Builder.h"
#import "Customer.h"
#import "Ticket.h"
#import "User.h"
#import "Comment.h"

@implementation Builder


+ (NSArray *)customersFromJSON:(NSData *)objectNotation error:(NSError **)error
{
    NSError *localError = nil;
    id jsonObject = [NSJSONSerialization JSONObjectWithData:objectNotation options:0 error:&localError];
    
    if (jsonObject == nil) {
        *error = localError;
        return nil;
    }
    
    NSDictionary *jsonDictionary = (NSDictionary *)jsonObject;
    NSMutableArray *customers = [[NSMutableArray alloc] init];
    NSError *cError = [[NSError alloc] init];
    
    // 1 user or many ?
    
    if([jsonDictionary valueForKey:@"customer"] != nil) {
        NSDictionary *customerDict = [jsonDictionary valueForKey:@"customer"];
        Customer* customer = [self customerFromJSON:customerDict error:&cError];
        if (customer == nil) {
            *error = cError;
            return nil;
        }
        [customers addObject:customer];
    }

    else if([jsonDictionary valueForKey:@"customer"] != nil) {
        
        NSArray *customerList = [jsonDictionary valueForKey:@"customers"];
        NSLog(@"Customer Count %lu", (unsigned long)customerList.count);
        
        for (NSDictionary *custDic in customerList) {
            
            Customer* customer = [self customerFromJSON:custDic error:&cError];
            if (customer == nil) {
                *error = cError;
                return nil;
            }
            [customers addObject:customer];
        }
    }
    else return nil;  // Error
    
    return customers;

}


+ (Customer *)customerFromJSON:(NSDictionary *)customerDic error:(NSError **)error
{
  
    Customer *customer = [[Customer alloc] init];

    // get the customer properties
    
        for (NSString *key in customerDic) {
            // test
            NSLog(@"Key  %s", key.UTF8String);
            
            if ([key isEqualToString:@"tickets"] )
            {
                NSLog(@"Processing Ticket");
                NSArray* tickets = [customerDic valueForKey:@"tickets"];
                
#warning //Bob might not be an array if only 1 ticket?
                
                //process each ticket in the array
                for (NSDictionary *tdict in tickets) {
                    // for each customer field
                    Ticket *tic = [[Ticket alloc] init];
                    
                    tic.id = [NSString stringWithFormat:@"%@", [tdict valueForKey:@"id"]];
                    NSLog(@"Read and set ticket id %@", [tic id]);
                    
                    tic.tnumber = [NSString stringWithFormat:@"%@", [tdict valueForKey:@"tnumber"]];
                    tic.ttype = [NSString stringWithFormat:@"%@", [tdict valueForKey:@"ttype"]];
                    tic.body = [NSString stringWithFormat:@"%@", [tdict valueForKey:@"body"]];
                    tic.timestamp = [NSString stringWithFormat:@"%@", [tdict valueForKey:@"timestamp"]];
                    tic.firstname = [NSString stringWithFormat:@"%@", [tdict valueForKey:@"firstname"]];
                    tic.lastname = [NSString stringWithFormat:@"%@", [tdict valueForKey:@"lastname"]];
                    tic.phone = [NSString stringWithFormat:@"%@", [tdict valueForKey:@"phone"]];
                    tic.cemail = [NSString stringWithFormat:@"%@", [tdict valueForKey:@"cemail"]];
                    tic.tstate = [NSString stringWithFormat:@"%@", [tdict valueForKey:@"tstate"]];
                    
                    // add ticket to customer
                    [customer addTicket:tic];
                }
                
            }
            
            if ([customer respondsToSelector:NSSelectorFromString(key)] && ![key isEqualToString:@"tickets" ]) {
                NSLog(@"Responded to Selector %s", key.UTF8String);
                
                
                // force all types to string before placing in the ticket obj
                NSString *sValue = [NSString stringWithFormat:@"%@", [customerDic valueForKey:key]];
                [customer setValue:sValue forKey:key];
                    
                    ///  [customer setValue:[customerDic valueForKey:key] forKey:key];
                    
                
            }
        }
  //  }
    return customer;

}

/*
+ (NSArray *)ticketsFromJSON:(NSData *)objectNotation error:(NSError **)error
{
    NSError *localError = nil;
    NSDictionary *parsedObject = [NSJSONSerialization JSONObjectWithData:objectNotation options:0 error:&localError];
    
    if (localError != nil) {
        *error = localError;
        return nil;
    }
    
    
    NSMutableArray *tickets = [[NSMutableArray alloc] init];
    
    NSArray *resources = [parsedObject valueForKey:@"objects"];
    NSLog(@"Ticket Count %lu", resources.count);
    
    for (NSDictionary *ticketsDic in resources) {
        Ticket *ticket = [[Ticket alloc] init];
        
        for (NSString *key in ticketsDic) {
            // test
            NSLog(@"Key  %s", key.UTF8String);
            if ([ticket respondsToSelector:NSSelectorFromString(key)]) {
                NSLog(@"Ticket Responded to Selector %s", key.UTF8String);
                
                NSLog(@"Type of ticket key is %@", NSStringFromClass([key class]));
                
                if(![key isEqualToString: @"self"])   {  // skip unfortunate keyword used as json obj attribute
                    
                        // force all types to string before placing in the ticket obj
                        NSString *sValue = [NSString stringWithFormat:@"%@", [ticketsDic valueForKey:key]];
                        [ticket setValue:sValue forKey:key];
                }
     
            }
        }
        
        [tickets addObject:ticket];
    }
    
    return tickets;
}

 */


+ (NSArray *)usersFromJSON:(NSData *)jsonData error:(NSError **)error
{
    NSError *localError = nil;
    id jsonObject = [NSJSONSerialization JSONObjectWithData:jsonData options:kNilOptions error:&localError];
    
    if (localError != nil) {
        *error = localError;
        return nil;
    }
    
    NSDictionary *jsonDictionary = (NSDictionary *)jsonObject;
    NSMutableArray *users = [[NSMutableArray alloc] init];
    NSError *cError = [[NSError alloc] init];
    
    // 1 user or many ?
  
    if([jsonDictionary valueForKey:@"user"] != nil) {
         NSDictionary *userDict = [jsonDictionary valueForKey:@"user"];
         User* user = [self userFromJSON:userDict error:&cError];
         if (user == nil) {
            *error = cError;
            return nil;
         }
         [users addObject:user];
    }
    
    else if([jsonDictionary valueForKey:@"users"] != nil) {
        
             NSArray *userList = [jsonDictionary valueForKey:@"users"];
             NSLog(@"User Count %lu", (unsigned long)userList.count);

             for (NSDictionary *usersDic in userList) {
      
                  User* user = [self userFromJSON:usersDic error:&cError];
                  if (user == nil) {
                      *error = cError;
                      return nil;
                  }
                  [users addObject:user];
             }
    }
         else return nil;  // Error
    
    return users;
}


+ (User * )userFromJSON:(NSDictionary *) userDic error:(NSError **) error
{
   User *user = [[User alloc] init];
   for (NSString *key in userDic) {
      // test
      NSLog(@"Key  %s", key.UTF8String);
    
      if ([key isEqualToString:@"customers"] )
      {
          NSArray* customers = [userDic valueForKey:@"customers"];
        
          //process each customer in the array
          for (NSDictionary *cdict in customers) {
              // for each customer field
              Customer *cust = [[Customer alloc] init];
            
              cust.cname = [NSString stringWithFormat:@"%@", [cdict valueForKey:@"cname"]];
              cust.id = [NSString stringWithFormat:@"%@", [cdict valueForKey:@"id"]];;
              cust.email = [NSString stringWithFormat:@"%@", [cdict valueForKey:@"email"]];
              cust.opentickets = [NSString stringWithFormat:@"%@", [cdict valueForKey:@"opentickets"]];
            
              // add cust to user
              [user addCustomer:cust];
          }
      }
    
      if ([user respondsToSelector:NSSelectorFromString(key)] && ![key isEqualToString:@"customers" ]) {
          NSLog(@"User Responded to Selector %s", key.UTF8String);
        
          NSLog(@"%@ ,Value associated with key is %@", [NSThread currentThread], [userDic valueForKey:key]);
        
          // force all types to string before placing in the ticket obj
          NSString *sValue = [NSString stringWithFormat:@"%@", [userDic valueForKey:key]];
          [user setValue:sValue forKey:key];
      }
   }
    
    return user;

}


+ (NSArray *)ticketsFromJSON:(NSData *)objectNotation error:(NSError **)error
{
    NSError *localError = nil;
    id jsonObject = [NSJSONSerialization JSONObjectWithData:objectNotation options:0 error:&localError];
    
    if (jsonObject == nil) {
        *error = localError;
        return nil;
    }
    
  
    NSDictionary *jsonDictionary = (NSDictionary *)jsonObject;
    NSMutableArray *tickets = [[NSMutableArray alloc] init];
    NSError *cError = [[NSError alloc] init];
    
    // 1 ticket or many ?
    
    if([jsonDictionary valueForKey:@"ticket"] != nil) {
        NSDictionary *userDict = [jsonDictionary valueForKey:@"ticket"];
        Ticket* ticket = [self ticketFromJSON:userDict error:&cError];
        if (ticket == nil) {
            *error = cError;
            return nil;
        }
        [tickets addObject:ticket];
    }
  
    else if([jsonDictionary valueForKey:@"tickets"] != nil) {
        
        NSArray *ticketList = [jsonDictionary valueForKey:@"tickets"];
        NSLog(@"Ticket Count %lu", (unsigned long)ticketList.count);
        
        for (NSDictionary *ticketDic in ticketList) {
            
            Ticket* ticket = [self ticketFromJSON:ticketDic error:&cError];
            if (ticket == nil) {
                *error = cError;
                return nil;
            }
            [tickets addObject:ticket];
        }
    }
    else return nil;  // Error
    
    return tickets;


}


+ (Ticket *)ticketFromJSON:(NSDictionary *)ticketDic error:(NSError **)error
{
    
    //  NSArray *resources = [objectNotation valueForKey:@"objects"];
    
    Ticket *ticket = [[Ticket alloc] init];
    
    // get the customer properties
    //  for (NSDictionary *ticketDic in resources) {   // 7 keys here
    
    for (NSString *key in ticketDic) {
        // test
        NSLog(@"Key  %s", key.UTF8String);
        
        if ([key isEqualToString:@"comments"] )
        {
            NSLog(@"Processing comments");
            NSArray* comments = [ticketDic valueForKey:@"comments"];
            
#warning //Bob might not be an array if only 1 comment?
            
            //process each comment in the array
            for (NSDictionary *cdict in comments) {
                Comment *comment = [self commentFromDict:cdict];
                
                // for each comment field
            //    Comment *comment = [[Comment alloc] init];
                
            //    comment.id = [NSString stringWithFormat:@"%@", [cdict valueForKey:@"id"]];
            //    NSLog(@"Read and set comment id %@", [comment id]);
            //    comment.user_id = [NSString stringWithFormat:@"%@", [cdict valueForKey:@"user_id"]];
            //    comment.ticket_id = [NSString stringWithFormat:@"%@", [cdict valueForKey:@"ticket_id"]];
            //    comment.timestamp = [NSString stringWithFormat:@"%@", [cdict valueForKey:@"timestamp"]];
            //    comment.body = [NSString stringWithFormat:@"%@", [cdict valueForKey:@"body"]];
            //    comment.notification = [NSString stringWithFormat:@"%@", [cdict valueForKey:@"notification"]];
               
                // add follower to ticket
                [ticket addComment:comment];
            }
            
        }
        
        if ([ticket respondsToSelector:NSSelectorFromString(key)] && ![key isEqualToString:@"comments" ]) {
            NSLog(@"Responded to Selector %s", key.UTF8String);
            
            if(![key isEqualToString: @"self"])  { // skip unfortunate keyword used as json obj attribute
                
                // force all types to string before placing in the ticket obj
                NSString *sValue = [NSString stringWithFormat:@"%@", [ticketDic valueForKey:key]];
                [ticket setValue:sValue forKey:key];
                
            }
        }
    }
    //  }
    return ticket;
    
}

+ (Comment *)commentFromDict:(NSDictionary *)cdict {
    
    Comment *comment = [[Comment alloc] init];
    
    for (NSString *key in cdict) {
        // test
        NSLog(@"Key  %s", key.UTF8String);
        
        // Get a few user fields of interest
        
        if ([key isEqualToString:@"user"] )
        {
           // No fields of interest
        }
   
        if ([comment respondsToSelector:NSSelectorFromString(key)] && ![key isEqualToString:@"user" ]) {
        
          // force all types to string before placing in the comment obj
          NSString *sValue = [NSString stringWithFormat:@"%@", [cdict valueForKey:key]];
          [comment setValue:sValue forKey:key];

        
     //    comment.id = [NSString stringWithFormat:@"%@", [cdict valueForKey:@"id"]];
     //     NSLog(@"Read and set comment id %@", [comment id]);
     //     comment.user_id = [NSString stringWithFormat:@"%@", [cdict valueForKey:@"user_id"]];
     //     comment.ticket_id = [NSString stringWithFormat:@"%@", [cdict valueForKey:@"ticket_id"]];
     //     comment.timestamp = [NSString stringWithFormat:@"%@", [cdict valueForKey:@"timestamp"]];
     //     comment.body = [NSString stringWithFormat:@"%@", [cdict valueForKey:@"body"]];
     //     comment.notification = [NSString stringWithFormat:@"%@", [cdict valueForKey:@"notification"]];
        }
        
    }
    return comment;
    
}

+ (NSArray *)commentsFromJSON:(NSData *)objectNotation error:(NSError **)error
{
    NSError *localError = nil;
    id jsonObject = [NSJSONSerialization JSONObjectWithData:objectNotation options:0 error:&localError];
    
    if (jsonObject == nil) {
        *error = localError;
        return nil;
    }
    
    
    NSDictionary* jsonDictionary;
    
    // Is it a dictionary containing an array of ticket objects?
    NSArray *jsonArray = [jsonObject valueForKey:@"objects"];
    if ([jsonArray count] > 0)
    {
        jsonDictionary = nil;
    }
    
    else {
        NSLog(@"its probably a dictionary with 1 comment");
        jsonDictionary = (NSDictionary *)jsonObject;
        
        NSLog(@"jsonDictionary - %@",jsonDictionary);
    }
    
    NSMutableArray *comments = [[NSMutableArray alloc] init];
    
    // More than 1 comment
    if( jsonDictionary == nil) {
        
        NSError *cError = [[NSError alloc] init];
        
        // Process each comment 1 at a time
        for ( NSDictionary* dict in jsonArray) {
            
            Comment* comm = [self commentFromDict:dict];
            if (comm == nil) {
          //      *error = cError;
                return nil;
            }
            
            [comments addObject:comm];
        }
    }
    else {
        NSError *cError = [[NSError alloc] init];
        
        Ticket* tict = [self ticketFromJSON:jsonDictionary error: &cError];
        if (tict == nil) {
            *error = cError;
            return nil;
        }
        NSLog(@"Ticket id is %@", [tict id]);
        [comments addObject:tict];
    }
    
    return comments;
}

+ (Comment *)commentFromJSON:(NSData *)objectNotation error:(NSError **)error
{
    NSError *localError = nil;
    id jsonObject = [NSJSONSerialization JSONObjectWithData:objectNotation options:0 error:&localError];
    
    if (jsonObject == nil) {
        *error = localError;
        return nil;
    }
    
    NSArray* jsonArray;
    NSDictionary* jsonDictionary;
    
    // More than 1 comment?
    if ([jsonObject isKindOfClass:[NSArray class]]) {
        NSLog(@"its an array!");
        jsonArray = (NSArray *)jsonObject;
        jsonDictionary = nil;
        NSLog(@"jsonArray - %@",jsonArray);
    }
    else {
        NSLog(@"its probably a dictionary");
        jsonDictionary = (NSDictionary *)jsonObject;
        NSLog(@"jsonDictionary - %@",jsonDictionary);
    }
    
    Comment *comment = [self commentFromDict:jsonDictionary];
    return comment;
    
}

/*
 if ([objectNotation isKindOfClass:[NSArray class]]) {
 if (error) {  // check for null
 
 NSString *domain = @"com.websterx.mCare.ErrorDomain";
 NSString *desc = NSLocalizedString(@"Expected 1 customer but query returned more than 1", @"");
 NSDictionary *userInfo = @{ NSLocalizedDescriptionKey : desc };
 *error = [NSError errorWithDomain:domain
 code:-101
 userInfo:userInfo];
 }
 return nil;
 }
 */


@end