//
//  LoginViewController.h
//  mCare
//
//  Created by Bob Webster on 12/16/14.
//  Copyright (c) 2014 vca. All rights reserved.
//

#import <UIKit/UIKit.h>
#import "CommunicatorDelegate.h"

@interface LoginViewController : UIViewController

@property (nonatomic, strong) NSString* userName;
@property (copy, nonatomic) IBOutlet NSString *userId;
@property (nonatomic, strong) NSString* cfRestUrl;

@end
