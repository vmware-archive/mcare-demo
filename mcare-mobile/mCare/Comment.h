//
//  Comment.h
//  mCare
//
//  Created by Bob Webster on 12/20/14.
//  Copyright (c) 2014 vca. All rights reserved.
//


#ifndef mCare_Comment_h
#define mCare_Comment_h

#import <UIKit/UIKit.h>

@interface Comment : NSObject
@property (strong, nonatomic) NSString *id;
@property (strong, nonatomic) NSString *ticket_id;
@property (strong, nonatomic) NSString *user_id;
@property (strong, nonatomic) NSString *email;
@property (strong, nonatomic) NSString *body;
@property (strong, nonatomic) NSString *timestamp;
@property (strong, nonatomic) NSString *notification;

@end

#endif
