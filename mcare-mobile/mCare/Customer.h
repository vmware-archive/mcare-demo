//
//  Customer.h
//  mCare
//
//  Created by Bob Webster on 12/14/14.
//  Copyright (c) 2014 vca. All rights reserved.
//

#ifndef mCare_Customer_h
#define mCare_Customer_h

#import <Foundation/Foundation.h>
#import "Ticket.h"

@interface Customer : NSObject

@property (strong, nonatomic) NSString *id;
@property (strong, nonatomic) NSString *cname;
@property (strong, nonatomic) NSString *email;
@property (strong, nonatomic) NSString *street;
@property (strong, nonatomic) NSString *city;
@property (strong, nonatomic) NSString *state;
@property (strong, nonatomic) NSString *postal;
@property (strong, nonatomic) NSString *opentickets;

- (void) addTicket:(Ticket*) t;
- (int)  numberOfOpenTickets;
@end


#endif
