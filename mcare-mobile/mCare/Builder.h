//
//  Builder.h
//  mCare
//
//  Created by Bob Webster on 12/14/14.
//  Copyright (c) 2014 vca. All rights reserved.
//

#ifndef mCare_Builder_h
#define mCare_Builder_h

#import <Foundation/Foundation.h>
#import "Comment.h"

@interface Builder : NSObject

+ (NSArray *)customersFromJSON:(NSData *)objectNotation error:(NSError **)error;
+ (NSArray *)ticketsFromJSON:(NSData *)objectNotation error:(NSError **)error;
+ (NSArray *)usersFromJSON:(NSData *)objectNotation error:(NSError **)error;
+ (NSArray *)commentsFromJSON:(NSData *)objectNotation error:(NSError **)error;
+ (Comment *)commentFromJSON:(NSData *)objectNotation error:(NSError **)error;
+ (Comment *)commentFromDict:(NSDictionary *)cdict;

@end

#endif
