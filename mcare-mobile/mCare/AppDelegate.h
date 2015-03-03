//
//  AppDelegate.h
//  mCare
//
//  Created by Bob Webster on 12/14/14.
//  Copyright (c) 2014 vca. All rights reserved.
//

#import <UIKit/UIKit.h>
#import "User.h"

@interface AppDelegate : UIResponder <UIApplicationDelegate>

@property (strong, nonatomic) UIWindow *window;
@property (nonatomic, strong) id signInDelegate;
@property (nonatomic, strong) NSString* userName;
@property (strong, nonatomic) User *user;
@property (nonatomic, strong) NSString* flaskUrl;

+ (void) callEndpoint:(NSString*)endpoint
               params:(NSDictionary*)params
      completionBlock:(void (^)(id results, NSError* error))completionBlock;


@end

