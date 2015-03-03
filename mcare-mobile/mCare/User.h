//
//  User.h
//  mCare
//
//  Created by Bob Webster on 12/14/14.
//  Copyright (c) 2014 vca. All rights reserved.
//

#ifndef mCare_User_h
#define mCare_User_h

#import "customer.h"

@interface User : NSObject
@property (strong, nonatomic) NSString *id;
@property (strong, nonatomic) NSString *uname;
@property (strong, nonatomic) NSString *firstname;
@property (strong, nonatomic) NSString *lastname;
@property (strong, nonatomic) NSString *phone;
@property (strong, nonatomic) NSString *email;
@property (strong, nonatomic) NSString *kinveyuser;
@property (strong, nonatomic) NSString *kinveypassword;
@property (retain, nonatomic) IBOutlet NSMutableArray *customers;

- (void) addCustomer:(Customer*) c;

@end

#endif

