//
//  Ticket.m
//  mCare
//
//  Created by Bob Webster on 12/15/14.
//  Copyright (c) 2014 vca. All rights reserved.
//


#import <Foundation/Foundation.h>
#import "Ticket.h"
#import "Comment.h"

// TODO Bob http://www.objc.io/issue-7/value-objects.html

@interface Ticket()



@end

@implementation Ticket


- (instancetype)init
{
    self = [super init];
    if (self) {
        self.id = @"";
        self.tnumber=@"";
        self.ttype=@"";
        self.body = @"";
        self.timestamp = @"";
        self.firstname = @"";
        self.lastname = @"";
        self.phone = @"";
        self.cemail = @"";
        self.tstate = @"";
        self.comments = [NSMutableArray array];  // do not do [[NSMutableArray alloc]init] 
        
    }
    return self;
}

- (BOOL)isEqual:(id)obj
{
    if(![obj isKindOfClass:[Ticket class]]) return NO;
    
    Ticket* other = (Ticket*)obj;
    
    BOOL timeIsEqual = self.timestamp == other.timestamp || [self.timestamp isEqual:other.timestamp];
    BOOL emailIsEqual = self.cemail == other.cemail || [self.cemail isEqual:other.cemail];
    return timeIsEqual && emailIsEqual;
}

-(NSString *)description
{
    return [NSString stringWithFormat:@"<Ticket: tnumber: %@ id: %@ ttype: %@ body %@ timestamp %@ firstname %@, \
                            lastname %@, phone %@, cemail %@, tstate %@,  comments %@>",  \
                            [self tnumber], [self id], [self ttype], [self body], [self timestamp], \
                            [self firstname], [self lastname], [self phone], [self cemail], \
                            [self tstate], [self comments]];
}

- (void) addComment:(Comment*) comment
{
    [_comments addObject:comment];
}

- (void) removeComment:(NSString*) id
{
    NSInteger count = [_comments count];
    for (NSInteger index = (count - 1); index >= 0; index--) {
        Comment *c = _comments[index];
        if ([c.id isEqualToString:id]) {
            [_comments removeObjectAtIndex:index];
        }
    }
}

@end