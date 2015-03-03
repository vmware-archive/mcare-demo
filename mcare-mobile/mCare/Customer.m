//
//  Customer.m
//  mCare
//
//  Created by Bob Webster on 12/14/14.
//  Copyright (c) 2014 vca. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "Customer.h"
#import "Ticket.h"

// TODO Bob http://www.objc.io/issue-7/value-objects.html

@interface Customer()

@property (retain, nonatomic) IBOutlet NSMutableArray *tickets;

@end

@implementation Customer


- (instancetype)init
{
    self = [super init];
    if (self) {
        self.id = @"";
        self.cname = @"";
        self.email = @"";
        self.street = @"";
        self.city = @"";
        self.state= @"";
        self.postal= @"";
        self.tickets = [[NSMutableArray alloc] init];
        self.opentickets = @"";

    }
    return self;
}

- (BOOL)isEqual:(id)obj
{
    if(![obj isKindOfClass:[Customer class]]) return NO;
    
    Customer* other = (Customer*)obj;
    
    BOOL nameIsEqual = self.cname == other.cname || [self.cname isEqual:other.cname];
    BOOL emailIsEqual = self.email == other.email || [self.email isEqual:other.email];
       return nameIsEqual && emailIsEqual;
}

-(NSString *)description
{
    return [NSString stringWithFormat:@"<Customer: id: %@ cname: %@ email %@ tickets %@>",
            [self id], [self cname], [self email], [self tickets]];
}

- (void) addTicket:(Ticket*) t
{
    [_tickets addObject:t];
}

//- (int) numberOfOpenTickets
//{
//    int open=0;
//    NSLog(@"%lu, %@", (unsigned long)[_tickets count], @"Tickets");
//    for (Ticket* t in _tickets) {
//        if([t tstate] != nil && [[t tstate] isEqualToString:(@"OPEN")])
//            open++;
//    }
//    return open;
//}

@end