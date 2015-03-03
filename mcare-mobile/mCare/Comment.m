//
//  Follower.m
//  mCare
//
//  Created by Bob Webster on 12/20/14.
//  Copyright (c) 2014 vca. All rights reserved.
//
//
//  Comment.m
//  mCare
//
//  Created by Bob Webster on 12/16/14.
//  Copyright (c) 2014 vca. All rights reserved.
//

#include "Comment.h"

@interface Comment()

@end



@implementation Comment

- (instancetype)init
{
    self = [super init];
    if (self) {
        self.id = @"";
        self.body = @"";
        self.notification = @"";
        self.timestamp = @"";
        self.ticket_id = @"";
        self.user_id = @"";
        self.email = @"";
    }
    return self;
}

- (BOOL)isEqual:(id)obj
{
    if(![obj isKindOfClass:[Comment class]]) return NO;
    
    Comment* other = (Comment*)obj;
    
    BOOL ticket_id = self.ticket_id == other.ticket_id || [self.ticket_id isEqual:other.ticket_id];
    BOOL timestamp = self.timestamp == other.timestamp || [self.timestamp isEqual:other.timestamp];
    return ticket_id && timestamp;
}


-(NSString *)description
{
    return [NSString stringWithFormat:@"<Ticket: id: %@ body: %@ notification %@ timestamp %@ ticket_id %@, user_id %@, email %@>",
            [self id], [self body], [self notification], [self timestamp], [self ticket_id], [self user_id], [self email]];
}


@end
