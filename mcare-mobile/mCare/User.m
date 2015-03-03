//
//  User.m
//  mCare
//
//  Created by Bob Webster on 12/16/14.
//  Copyright (c) 2014 vca. All rights reserved.
//

#import <Foundation/Foundation.h>
#include "User.h"
#include "Customer.h"

@interface User()



@end



@implementation User

- (instancetype)init
{
    self = [super init];
    if (self) {
        self.id = @"";
        self.uname = @"";
        self.firstname = @"";
        self.lastname = @"";
        self.phone = @"";
        self.email = @"";
        self.kinveyuser = @"";
        self.kinveypassword = @"";
        self.customers =  [NSMutableArray array]  ;   //not on class [[NSMutableArray alloc] init];
    }
    return self;
}

-(NSString *)description
{
    return [NSString stringWithFormat:@"<User: id: %@ uname: %@ firstname %@ lastname %@ phone %@, email %@, \
            kinveyuser %@, kinveypassword %@,customers %@>",
            [self id], [self uname], [self firstname], [self lastname], [self phone], [self email],
            [self kinveyuser], [self kinveypassword], [self customers] ];
}

- (BOOL)isEqual:(id)obj
{
    if(![obj isKindOfClass:[User class]]) return NO;
    
    User* other = (User*)obj;
    
    BOOL emailIsEqual = self.email == other.email || [self.email isEqual:other.email];
    BOOL lastnameIsEqual = self.lastname == other.lastname || [self.lastname isEqual:other.lastname];
    return emailIsEqual && lastnameIsEqual;
}

- (void) addCustomer:(Customer*) c
{
       [_customers addObject:c];
}

@end
