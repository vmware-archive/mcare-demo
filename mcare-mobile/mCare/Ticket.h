//
//  Ticket.h
//  mCare
//
//  Created by Bob Webster on 12/14/14.
//  Copyright (c) 2014 vca. All rights reserved.
//

#ifndef mCare_Ticket_h
#define mCare_Ticket_h

#import "Comment.h"


@interface Ticket : NSObject

@property (strong, nonatomic) NSString *id;
@property (strong, nonatomic) NSString *tnumber;
@property (strong, nonatomic) NSString *ttype;
@property (strong, nonatomic) NSString *body;
@property (strong, nonatomic) NSString *timestamp;
@property (strong, nonatomic) NSString *firstname;
@property (strong, nonatomic) NSString *lastname;
@property (strong, nonatomic) NSString *phone;
@property (strong, nonatomic) NSString *cemail;
@property (strong, nonatomic) NSString *tstate;
@property (strong, nonatomic) NSMutableArray *comments;


- (void) addComment:(Comment*) comment;
- (void) removeComment:(NSString*) id;
@end

#endif
